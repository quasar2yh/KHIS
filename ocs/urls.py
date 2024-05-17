from django.urls import path
from . import views

urlpatterns = [
    path('', views.MedicalRecordAPIView.as_view()),
    path('<int:patient_id>/', views.MedicalRecordAPIView.as_view()),
    path('<int:patient_id>/<int:medical_record_id>/', views.MedicalRecordAPIView.as_view())
]