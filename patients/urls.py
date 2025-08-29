from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/new/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),

    path('payments/new/', views.payment_create, name='payment_create'),
    path('patients/<int:patient_pk>/payments/new/', views.payment_create, name='patient_payment_create'),

    path('visits/new/', views.visit_create, name='visit_create'),
    path('patients/<int:patient_pk>/visits/new/', views.visit_create, name='patient_visit_create'),

    path('xrays/new/', views.xray_create, name='xray_create'),
    path('patients/<int:patient_pk>/xrays/new/', views.xray_create, name='patient_xray_create'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]