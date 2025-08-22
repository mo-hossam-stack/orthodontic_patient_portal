from django.contrib import admin
from .models import Patient, Payment, Visit, XRay


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'join_date', 'photo')
    search_fields = ('name', 'phone_number')
    list_filter = ('join_date',)
    readonly_fields = ('join_date',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'phone_number', 'photo')
        }),
        ('Additional Information', {
            'fields': ('notes', 'join_date')
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'total_amount', 'paid_amount', 'remaining_amount', 'last_update')
    search_fields = ('patient__name',)
    list_filter = ('last_update',)
    readonly_fields = ('remaining_amount', 'last_update')
    fieldsets = (
        ('Payment Information', {
            'fields': ('patient', 'total_amount', 'paid_amount')
        }),
        ('Calculated Fields', {
            'fields': ('remaining_amount', 'last_update'),
            'classes': ('collapse',)
        }),
    ) 


@admin.register(XRay)
class XRayAdmin(admin.ModelAdmin):
    list_display = ('patient', 'image', 'date_added')
    search_fields = ('patient__name',)
    list_filter = ('date_added',)
    readonly_fields = ('date_added',)
    fieldsets = (
        ('X-Ray Information', {
            'fields': ('patient', 'image')
        }),
        ('Metadata', {
            'fields': ('date_added',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'visit_date', 'xray', 'payment_this_visit')
    search_fields = ('patient__name', 'notes')
    list_filter = ('visit_date', 'xray')
    fieldsets = (
        ('Visit Information', {
            'fields': ('patient', 'visit_date', 'notes')
        }),
        ('Related Items', {
            'fields': ('xray', 'payment_this_visit'),
            'classes': ('collapse',)
        }),
    )

