from django import forms
from .models import Patient, Payment, Visit, XRay


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone_number', 'photo', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css_classes + ' form-control').strip()


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['patient', 'total_amount', 'paid_amount']
        widgets = {
            'total_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'paid_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css_classes + ' form-control').strip()

    def clean(self):
        cleaned_data = super().clean()
        total_amount = cleaned_data.get('total_amount')
        paid_amount = cleaned_data.get('paid_amount')
        
        if total_amount and paid_amount and paid_amount > total_amount:
            raise forms.ValidationError("Paid amount cannot exceed total amount.")
        
        return cleaned_data


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['patient', 'visit_date', 'notes', 'xray', 'payment_this_visit']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_this_visit': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css_classes + ' form-control').strip()


class XRayForm(forms.ModelForm):
    class Meta:
        model = XRay
        fields = ['patient', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css_classes + ' form-control').strip()