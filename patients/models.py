from django.db import models

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='patients/photos/', blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.patient.name} - Payment {self.id}"

    def save(self, *args, **kwargs):
        # Automatically calculate remaining amount
        self.remaining_amount = self.total_amount - self.paid_amount
        super().save(*args, **kwargs)

class XRay(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='xrays')
    image = models.ImageField(upload_to='patients/xrays/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.patient.name} - X-ray {self.id}"