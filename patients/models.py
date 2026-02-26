from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="patients/photos/", blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="payments"
    )
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

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(paid_amount__lte=models.F("total_amount")),
                name="paid_cannot_exceed_total",
            ),
        ]


class XRay(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="xrays")
    image = models.ImageField(upload_to="patients/xrays/")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.patient.name} - X-ray {self.id}"


class Visit(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="visits"
    )
    visit_date = models.DateField()
    notes = models.TextField(blank=True)
    xray = models.ForeignKey(
        XRay, on_delete=models.SET_NULL, null=True, blank=True, related_name="visits"
    )
    payment_this_visit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.patient.name} - Visit {self.visit_date}"


class Appointment(models.Model):
    """Model for scheduling patient appointments."""

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        NO_SHOW = "no_show", "No Show"

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SCHEDULED
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appointments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.patient.name} - {self.datetime_start}"


class TreatmentPlan(models.Model):
    """Model for patient treatment plans."""

    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="treatment_plans"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PLANNED
    )
    start_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.patient.name} - {self.title}"


class Procedure(models.Model):

    treatment_plan = models.ForeignKey(
        TreatmentPlan, on_delete=models.CASCADE, related_name="procedures"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_performed = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.treatment_plan.title} - {self.name}"


# Signal receivers to delete files when records are deleted
@receiver(post_delete, sender=XRay)
def delete_xray_file(sender, instance, **kwargs):
    """Delete X-ray image file from storage when XRay record is deleted."""
    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=Patient)
def delete_patient_photo(sender, instance, **kwargs):
    """Delete patient photo from storage when Patient record is deleted."""
    if instance.photo:
        instance.photo.delete(save=False)
