from django.urls import path
from . import views

app_name = 'ocs'
urlpatterns = [
    path('patient-registration/', views.PatientAPIView.as_view()),
    path('patient-registration/<int:patient_id>/', views.PatientAPIView.as_view()),
    path('consultations/<int:patient_id>/', views.MedicalRecordAPIView.as_view()),
]