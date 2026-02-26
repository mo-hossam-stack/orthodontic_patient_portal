from django.contrib import admin
from .models import Patient, Payment, Visit, XRay, Appointment, TreatmentPlan, Procedure


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "join_date", "photo")
    search_fields = ("name", "phone_number")
    list_filter = ("join_date",)
    readonly_fields = ("join_date",)
    fieldsets = (
        ("Basic Information", {"fields": ("name", "phone_number", "photo")}),
        ("Additional Information", {"fields": ("notes", "join_date")}),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "total_amount",
        "paid_amount",
        "remaining_amount",
        "last_update",
    )
    search_fields = ("patient__name",)
    list_filter = ("last_update",)
    readonly_fields = ("remaining_amount", "last_update")
    fieldsets = (
        ("Payment Information", {"fields": ("patient", "total_amount", "paid_amount")}),
        (
            "Calculated Fields",
            {"fields": ("remaining_amount", "last_update"), "classes": ("collapse",)},
        ),
    )


@admin.register(XRay)
class XRayAdmin(admin.ModelAdmin):
    list_display = ("patient", "image", "date_added")
    search_fields = ("patient__name",)
    list_filter = ("date_added",)
    readonly_fields = ("date_added",)
    fieldsets = (
        ("X-Ray Information", {"fields": ("patient", "image")}),
        ("Metadata", {"fields": ("date_added",), "classes": ("collapse",)}),
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("patient", "visit_date", "xray", "payment_this_visit")
    search_fields = ("patient__name", "notes")
    list_filter = ("visit_date", "xray")
    fieldsets = (
        ("Visit Information", {"fields": ("patient", "visit_date", "notes")}),
        (
            "Related Items",
            {"fields": ("xray", "payment_this_visit"), "classes": ("collapse",)},
        ),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "datetime_start", "datetime_end", "status", "created_by")
    search_fields = ("patient__name", "notes")
    list_filter = ("status", "datetime_start")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Appointment Information",
            {"fields": ("patient", "datetime_start", "datetime_end", "status")},
        ),
        ("Notes", {"fields": ("notes",)}),
        (
            "Metadata",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "title",
        "status",
        "start_date",
        "expected_end_date",
        "created_at",
    )
    search_fields = ("patient__name", "title", "description")
    list_filter = ("status", "start_date", "expected_end_date")
    readonly_fields = ("created_at",)
    fieldsets = (
        (
            "Treatment Plan Information",
            {"fields": ("patient", "title", "description", "status")},
        ),
        ("Dates", {"fields": ("start_date", "expected_end_date", "actual_end_date")}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("treatment_plan", "name", "date_performed", "cost")
    search_fields = ("treatment_plan__title", "name", "description")
    list_filter = ("date_performed",)
    fieldsets = (
        (
            "Procedure Information",
            {"fields": ("treatment_plan", "name", "description")},
        ),
        ("Details", {"fields": ("date_performed", "cost", "notes")}),
    )