from django.urls import path
from . import views

app_name = 'ocs'
urlpatterns = [
    path('consultations/', views.MedicalRecordAPIView.as_view()),
    path('consultations/<int:patient_id>/', views.MedicalRecordAPIView.as_view()),
]