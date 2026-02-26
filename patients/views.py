from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from decimal import Decimal
from .models import Patient, Payment, Visit, XRay, Appointment, TreatmentPlan, Procedure
from django.contrib import messages
from .forms import (
    PatientForm,
    PaymentForm,
    VisitForm,
    XRayForm,
    AppointmentForm,
    TreatmentPlanForm,
    ProcedureForm,
)


@login_required
def dashboard(request):
    query = request.GET.get("q", "").strip()

    # Use annotate to avoid N+1 query problem
    patients_qs = (
        Patient.objects.all()
        .order_by("name")
        .annotate(
            total_owed=Coalesce(
                Sum("payments__remaining_amount"),
                Decimal("0"),
                output_field=DecimalField(),
            ),
            visit_count=Count("visits"),
        )
    )

    if query:
        patients_qs = patients_qs.filter(
            Q(name__icontains=query) | Q(phone_number__icontains=query)
        )

    paginator = Paginator(patients_qs, 12)
    page_number = request.GET.get("page")
    patients_page = paginator.get_page(page_number)

    return render(
        request,
        "patients/dashboard.html",
        {
            "patients": patients_page,
            "query": query,
        },
    )


@login_required
def patient_detail(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    payments = Payment.objects.filter(patient=patient).order_by("-last_update")
    visits = Visit.objects.filter(patient=patient).order_by("-visit_date")
    xrays = XRay.objects.filter(patient=patient).order_by("-date_added")

    # Calculate totals
    total_owed = payments.aggregate(total=Sum("remaining_amount"))["total"] or 0
    total_paid = payments.aggregate(total=Sum("paid_amount"))["total"] or 0

    return render(
        request,
        "patients/patient_detail.html",
        {
            "patient": patient,
            "payments": payments,
            "visits": visits,
            "xrays": xrays,
            "total_owed": total_owed,
            "total_paid": total_paid,
        },
    )


@login_required
def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient "{patient.name}" created successfully!')
            return redirect("patient_detail", pk=patient.pk)
    else:
        form = PatientForm()

    return render(
        request,
        "patients/patient_form.html",
        {
            "form": form,
            "title": "Add New Patient",
        },
    )


@login_required
def patient_edit(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient "{patient.name}" updated successfully!')
            return redirect("patient_detail", pk=patient.pk)
    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        "patients/patient_form.html",
        {
            "form": form,
            "title": f"Edit Patient: {patient.name}",
            "patient": patient,
        },
    )


@login_required
def payment_create(request, patient_pk: int = None):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f"Payment record created successfully!")
            return redirect("patient_detail", pk=payment.patient.pk)
    else:
        initial = {}
        if patient_pk:
            initial["patient"] = patient_pk
        form = PaymentForm(initial=initial)

    return render(
        request,
        "patients/payment_form.html",
        {
            "form": form,
            "title": "Add New Payment",
        },
    )


@login_required
def visit_create(request, patient_pk: int = None):
    if request.method == "POST":
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save()
            messages.success(request, f"Visit record created successfully!")
            return redirect("patient_detail", pk=visit.patient.pk)
    else:
        initial = {}
        if patient_pk:
            initial["patient"] = patient_pk
        form = VisitForm(initial=initial)

    return render(
        request,
        "patients/visit_form.html",
        {
            "form": form,
            "title": "Add New Visit",
        },
    )


@login_required
def xray_create(request, patient_pk: int = None):
    if request.method == "POST":
        form = XRayForm(request.POST, request.FILES)
        if form.is_valid():
            xray = form.save()
            messages.success(request, f"X-Ray record created successfully!")
            return redirect("patient_detail", pk=xray.patient.pk)
    else:
        initial = {}
        if patient_pk:
            initial["patient"] = patient_pk
        form = XRayForm(initial=initial)

    return render(
        request,
        "patients/xray_form.html",
        {
            "form": form,
            "title": "Add New X-Ray",
        },
    )


@login_required
def patient_delete(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        patient_name = patient.name
        patient.delete()
        messages.success(
            request, f'Patient "{patient_name}" has been deleted successfully'
        )
        return redirect("dashboard")

    return render(
        request,
        "patients/patient_delete_confirm.html",
        {
            "patient": patient,
        },
    )


# ===== Appointment Views =====


@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related("patient").order_by(
        "-datetime_start"
    )
    return render(
        request,
        "patients/appointment_list.html",
        {"appointments": appointments},
    )


@login_required
def appointment_create(request, patient_pk: int = None):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, "Appointment scheduled successfully!")
            if appointment.patient:
                return redirect("patient_detail", pk=appointment.patient.pk)
            return redirect("appointment_list")
    else:
        initial = {}
        if patient_pk:
            initial["patient"] = patient_pk
        form = AppointmentForm(initial=initial)

    return render(
        request,
        "patients/appointment_form.html",
        {"form": form, "title": "Schedule Appointment"},
    )


@login_required
def appointment_edit(request, pk: int):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, "Appointment updated successfully!")
            if appointment.patient:
                return redirect("patient_detail", pk=appointment.patient.pk)
            return redirect("appointment_list")
    else:
        form = AppointmentForm(instance=appointment)

    return render(
        request,
        "patients/appointment_form.html",
        {"form": form, "title": "Edit Appointment"},
    )


@login_required
def appointment_delete(request, pk: int):
    appointment = get_object_or_404(Appointment, pk=pk)
    patient_pk = appointment.patient.pk
    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Appointment cancelled successfully!")
        return redirect("patient_detail", pk=patient_pk)

    return render(
        request,
        "patients/appointment_delete_confirm.html",
        {"appointment": appointment},
    )


# ===== Treatment Plan Views =====


@login_required
def treatment_plan_list(request):
    treatment_plans = TreatmentPlan.objects.select_related("patient").order_by(
        "-created_at"
    )
    return render(
        request,
        "patients/treatment_plan_list.html",
        {"treatment_plans": treatment_plans},
    )


@login_required
def treatment_plan_create(request, patient_pk: int = None):
    if request.method == "POST":
        form = TreatmentPlanForm(request.POST)
        if form.is_valid():
            treatment_plan = form.save()
            messages.success(request, "Treatment plan created successfully!")
            if treatment_plan.patient:
                return redirect("patient_detail", pk=treatment_plan.patient.pk)
            return redirect("treatment_plan_list")
    else:
        initial = {}
        if patient_pk:
            initial["patient"] = patient_pk
        form = TreatmentPlanForm(initial=initial)

    return render(
        request,
        "patients/treatment_plan_form.html",
        {"form": form, "title": "Create Treatment Plan"},
    )


@login_required
def treatment_plan_edit(request, pk: int):
    treatment_plan = get_object_or_404(TreatmentPlan, pk=pk)
    if request.method == "POST":
        form = TreatmentPlanForm(request.POST, instance=treatment_plan)
        if form.is_valid():
            treatment_plan = form.save()
            messages.success(request, "Treatment plan updated successfully!")
            if treatment_plan.patient:
                return redirect("patient_detail", pk=treatment_plan.patient.pk)
            return redirect("treatment_plan_list")
    else:
        form = TreatmentPlanForm(instance=treatment_plan)

    return render(
        request,
        "patients/treatment_plan_form.html",
        {"form": form, "title": "Edit Treatment Plan"},
    )


@login_required
def treatment_plan_delete(request, pk: int):
    treatment_plan = get_object_or_404(TreatmentPlan, pk=pk)
    patient_pk = treatment_plan.patient.pk
    if request.method == "POST":
        treatment_plan.delete()
        messages.success(request, "Treatment plan deleted successfully!")
        return redirect("patient_detail", pk=patient_pk)

    return render(
        request,
        "patients/treatment_plan_delete_confirm.html",
        {"treatment_plan": treatment_plan},
    )


# ===== Procedure Views =====


@login_required
def procedure_create(request, treatment_plan_pk: int = None):
    if request.method == "POST":
        form = ProcedureForm(request.POST)
        if form.is_valid():
            procedure = form.save()
            messages.success(request, "Procedure added successfully!")
            if procedure.treatment_plan and procedure.treatment_plan.patient:
                return redirect(
                    "patient_detail", pk=procedure.treatment_plan.patient.pk
                )
            return redirect("treatment_plan_list")
    else:
        initial = {}
        if treatment_plan_pk:
            initial["treatment_plan"] = treatment_plan_pk
        form = ProcedureForm(initial=initial)

    return render(
        request,
        "patients/procedure_form.html",
        {"form": form, "title": "Add Procedure"},
    )


@login_required
def procedure_edit(request, pk: int):
    procedure = get_object_or_404(Procedure, pk=pk)
    if request.method == "POST":
        form = ProcedureForm(request.POST, instance=procedure)
        if form.is_valid():
            procedure = form.save()
            messages.success(request, "Procedure updated successfully!")
            if procedure.treatment_plan and procedure.treatment_plan.patient:
                return redirect(
                    "patient_detail", pk=procedure.treatment_plan.patient.pk
                )
            return redirect("treatment_plan_list")
    else:
        form = ProcedureForm(instance=procedure)

    return render(
        request,
        "patients/procedure_form.html",
        {"form": form, "title": "Edit Procedure"},
    )


@login_required
def procedure_delete(request, pk: int):
    procedure = get_object_or_404(Procedure, pk=pk)
    patient_pk = procedure.treatment_plan.patient.pk
    if request.method == "POST":
        procedure.delete()
        messages.success(request, "Procedure deleted successfully!")
        return redirect("patient_detail", pk=patient_pk)

    return render(
        request,
        "patients/procedure_delete_confirm.html",
        {"procedure": procedure},
    )


# ===== Payment Edit/Delete Views =====


@login_required
def payment_edit(request, pk: int):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            messages.success(request, "Payment updated successfully!")
            return redirect("patient_detail", pk=payment.patient.pk)
    else:
        form = PaymentForm(instance=payment)

    return render(
        request,
        "patients/payment_form.html",
        {"form": form, "title": "Edit Payment"},
    )


@login_required
def payment_delete(request, pk: int):
    payment = get_object_or_404(Payment, pk=pk)
    patient_pk = payment.patient.pk
    if request.method == "POST":
        payment.delete()
        messages.success(request, "Payment deleted successfully!")
        return redirect("patient_detail", pk=patient_pk)

    return render(
        request,
        "patients/payment_delete_confirm.html",
        {"payment": payment},
    )


# ===== Visit Edit/Delete Views =====


@login_required
def visit_edit(request, pk: int):
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == "POST":
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            visit = form.save()
            messages.success(request, "Visit updated successfully!")
            return redirect("patient_detail", pk=visit.patient.pk)
    else:
        form = VisitForm(instance=visit)

    return render(
        request,
        "patients/visit_form.html",
        {"form": form, "title": "Edit Visit"},
    )


@login_required
def visit_delete(request, pk: int):
    visit = get_object_or_404(Visit, pk=pk)
    patient_pk = visit.patient.pk
    if request.method == "POST":
        visit.delete()
        messages.success(request, "Visit deleted successfully!")
        return redirect("patient_detail", pk=patient_pk)

    return render(
        request,
        "patients/visit_delete_confirm.html",
        {"visit": visit},
    )


# ===== XRay Edit/Delete Views =====


@login_required
def xray_edit(request, pk: int):
    xray = get_object_or_404(XRay, pk=pk)
    if request.method == "POST":
        form = XRayForm(request.POST, request.FILES, instance=xray)
        if form.is_valid():
            xray = form.save()
            messages.success(request, "X-Ray updated successfully!")
            return redirect("patient_detail", pk=xray.patient.pk)
    else:
        form = XRayForm(instance=xray)

    return render(
        request,
        "patients/xray_form.html",
        {"form": form, "title": "Edit X-Ray"},
    )


@login_required
def xray_delete(request, pk: int):
    xray = get_object_or_404(XRay, pk=pk)
    patient_pk = xray.patient.pk
    if request.method == "POST":
        # Delete the file from storage
        if xray.image:
            xray.image.delete(save=False)
        xray.delete()
        messages.success(request, "X-Ray deleted successfully!")
        return redirect("patient_detail", pk=patient_pk)

    return render(
        request,
        "patients/xray_delete_confirm.html",
        {"xray": xray},
    )
