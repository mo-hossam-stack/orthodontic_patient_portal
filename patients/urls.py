from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("patients/new/", views.patient_create, name="patient_create"),
    path("patients/<int:pk>/edit/", views.patient_edit, name="patient_edit"),
    path("patients/<int:pk>/delete/", views.patient_delete, name="patient_delete"),
    # Payment URLs
    path("payments/new/", views.payment_create, name="payment_create"),
    path(
        "patients/<int:patient_pk>/payments/new/",
        views.payment_create,
        name="patient_payment_create",
    ),
    path("payments/<int:pk>/edit/", views.payment_edit, name="payment_edit"),
    path("payments/<int:pk>/delete/", views.payment_delete, name="payment_delete"),
    # Visit URLs
    path("visits/new/", views.visit_create, name="visit_create"),
    path(
        "patients/<int:patient_pk>/visits/new/",
        views.visit_create,
        name="patient_visit_create",
    ),
    path("visits/<int:pk>/edit/", views.visit_edit, name="visit_edit"),
    path("visits/<int:pk>/delete/", views.visit_delete, name="visit_delete"),
    # X-Ray URLs
    path("xrays/new/", views.xray_create, name="xray_create"),
    path(
        "patients/<int:patient_pk>/xrays/new/",
        views.xray_create,
        name="patient_xray_create",
    ),
    path("xrays/<int:pk>/edit/", views.xray_edit, name="xray_edit"),
    path("xrays/<int:pk>/delete/", views.xray_delete, name="xray_delete"),
    # Appointment URLs
    path("appointments/", views.appointment_list, name="appointment_list"),
    path("appointments/new/", views.appointment_create, name="appointment_create"),
    path(
        "patients/<int:patient_pk>/appointments/new/",
        views.appointment_create,
        name="patient_appointment_create",
    ),
    path(
        "appointments/<int:pk>/edit/", views.appointment_edit, name="appointment_edit"
    ),
    path(
        "appointments/<int:pk>/delete/",
        views.appointment_delete,
        name="appointment_delete",
    ),
    # Treatment Plan URLs
    path("treatment-plans/", views.treatment_plan_list, name="treatment_plan_list"),
    path(
        "treatment-plans/new/",
        views.treatment_plan_create,
        name="treatment_plan_create",
    ),
    path(
        "patients/<int:patient_pk>/treatment-plans/new/",
        views.treatment_plan_create,
        name="patient_treatment_plan_create",
    ),
    path(
        "treatment-plans/<int:pk>/edit/",
        views.treatment_plan_edit,
        name="treatment_plan_edit",
    ),
    path(
        "treatment-plans/<int:pk>/delete/",
        views.treatment_plan_delete,
        name="treatment_plan_delete",
    ),
    # Procedure URLs
    path("procedures/new/", views.procedure_create, name="procedure_create"),
    path(
        "treatment-plans/<int:treatment_plan_pk>/procedures/new/",
        views.procedure_create,
        name="treatment_plan_procedure_create",
    ),
    path("procedures/<int:pk>/edit/", views.procedure_edit, name="procedure_edit"),
    path(
        "procedures/<int:pk>/delete/", views.procedure_delete, name="procedure_delete"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
