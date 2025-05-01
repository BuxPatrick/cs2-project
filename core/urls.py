from django.urls import path
from . import views, api

app_name = 'core'

urlpatterns = [
    # Authentication URLs
    path('', views.role_selection, name='role_selection'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Dashboard URLs
    path('technician/', views.technician_dashboard, name='technician_dashboard'),
    path('neurologist/', views.neurologist_dashboard, name='neurologist_dashboard'),

    # Patient URLs
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/register/', views.patient_register, name='patient_register'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/vitals/', views.record_vitals, name='record_vitals'),
    path('patients/<int:patient_id>/nihss/', views.record_nihss, name='record_nihss'),
    path('patients/<int:patient_id>/consultation/', views.add_consultation, name='add_consultation'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),

    # Alert URLs
    path('alerts/<int:alert_id>/resolve/', views.resolve_alert, name='resolve_alert'),
    
    # API URLs
    path('api/simulate-patient-data/', api.simulate_patient_data, name='simulate_patient_data'),
]
