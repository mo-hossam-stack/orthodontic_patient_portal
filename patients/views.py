from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import Patient,Payment ,Visit,XRay
from django.contrib import messages
from .forms import PatientForm,PaymentForm,VisitForm,XRayForm
@login_required
def dashboard(request):
    query = request.GET.get('q', '').strip()
    patients_qs = Patient.objects.all().order_by('name')
    
    if query:
        patients_qs = patients_qs.filter(
            Q(name__icontains=query) | Q(phone_number__icontains=query)
        )
    
    # Add payment summary for each patient
    for patient in patients_qs:
        patient.total_owed = Payment.objects.filter(patient=patient).aggregate(
            total=Sum('remaining_amount')
        )['total'] or 0
        patient.visit_count = Visit.objects.filter(patient=patient).count()
    
    paginator = Paginator(patients_qs, 12)
    page_number = request.GET.get('page')
    patients_page = paginator.get_page(page_number)
    
    return render(request, 'patients/dashboard.html', {
        'patients': patients_page,
        'query': query,
    })


@login_required
def patient_detail(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    payments = Payment.objects.filter(patient=patient).order_by('-last_update')
    visits = Visit.objects.filter(patient=patient).order_by('-visit_date')
    xrays = XRay.objects.filter(patient=patient).order_by('-date_added')
    
    # Calculate totals
    total_owed = payments.aggregate(total=Sum('remaining_amount'))['total'] or 0
    total_paid = payments.aggregate(total=Sum('paid_amount'))['total'] or 0
    
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'payments': payments,
        'visits': visits,
        'xrays': xrays,
        'total_owed': total_owed,
        'total_paid': total_paid,
    })


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient "{patient.name}" created successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    
    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Add New Patient',
    })


@login_required
def patient_edit(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient "{patient.name}" updated successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': f'Edit Patient: {patient.name}',
    })


@login_required
def payment_create(request, patient_pk: int = None):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f'Payment record created successfully!')
            return redirect('patient_detail', pk=payment.patient.pk)
    else:
        initial = {}
        if patient_pk:
            initial['patient'] = patient_pk
        form = PaymentForm(initial=initial)
    
    return render(request, 'patients/payment_form.html', {
        'form': form,
        'title': 'Add New Payment',
    })


@login_required
def visit_create(request, patient_pk: int = None):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save()
            messages.success(request, f'Visit record created successfully!')
            return redirect('patient_detail', pk=visit.patient.pk)
    else:
        initial = {}
        if patient_pk:
            initial['patient'] = patient_pk
        form = VisitForm(initial=initial)
    
    return render(request, 'patients/visit_form.html', {
        'form': form,
        'title': 'Add New Visit',
    })

@login_required
def xray_create(request, patient_pk: int = None):
    if request.method == 'POST':
        form = XRayForm(request.POST, request.FILES)
        if form.is_valid():
            xray = form.save()
            messages.success(request, f'X-Ray record created successfully!')
            return redirect('patient_detail', pk=xray.patient.pk)
    else:
        initial = {}
        if patient_pk:
            initial['patient'] = patient_pk
        form = XRayForm(initial=initial)
    
    return render(request, 'patients/xray_form.html', {
        'form': form,
        'title': 'Add New X-Ray',
    })

def patient_delete(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient_name = patient.name
        patient.delete()
        messages.success(request, f'Patient "{patient_name}" has been deleted sucessfully')
        return redirect('dashboard')
    
    return render(request, 'patients/patient_delete_confirm.html', {
        'patient': patient,
    })  