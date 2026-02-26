from django import forms
from .models import Patient, Payment, Visit, XRay, Appointment, TreatmentPlan, Procedure


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["name", "phone_number", "photo", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_classes + " form-control").strip()


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["patient", "total_amount", "paid_amount"]
        widgets = {
            "total_amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "paid_amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_classes + " form-control").strip()

    def clean(self):
        cleaned_data = super().clean()
        total_amount = cleaned_data.get("total_amount")
        paid_amount = cleaned_data.get("paid_amount")

        if total_amount and paid_amount and paid_amount > total_amount:
            raise forms.ValidationError("Paid amount cannot exceed total amount.")

        return cleaned_data


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ["patient", "visit_date", "notes", "xray", "payment_this_visit"]
        widgets = {
            "visit_date": forms.DateInput(attrs={"type": "date"}),
            "payment_this_visit": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop("patient", None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_classes + " form-control").strip()

        # Filter X-Ray queryset to only show X-rays for the selected patient
        if patient:
            self.fields["xray"].queryset = XRay.objects.filter(patient=patient)


class XRayForm(forms.ModelForm):
    class Meta:
        model = XRay
        fields = ["patient", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_classes + " form-control").strip()


# ===== Appointment Forms =====


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "datetime_start", "datetime_end", "status", "notes"]
        widgets = {
            "datetime_start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "datetime_end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_classes + " form-control").strip()

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("datetime_start")
        end = cleaned_data.get("datetime_end")

        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data


# ===== Treatment Plan Forms =====


class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = [
            "patient",
            "title",
            "description",
            "status",
            "start_date",
            "expected_end_date",
            "actual_end_date",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g., Braces Treatment"}),
            "description": forms.Textarea(attrs={"rows": 3}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "expected_end_date": forms.DateInput(attrs={"type": "date"}),
            "actual_end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_classes + " form-control").strip()


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = [
            "treatment_plan",
            "name",
            "description",
            "date_performed",
            "cost",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g., Bracket Placement"}),
            "description": forms.Textarea(attrs={"rows": 2}),
            "date_performed": forms.DateInput(attrs={"type": "date"}),
            "cost": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_classes + " form-control").strip()
