from django.urls import path
from . import views

urlpatterns = [
    path('', views.MedicalRecordAPIView.as_view()),
    path('<int:patient_id>/', views.MedicalRecordAPIView.as_view()),
    path('<int:patient_id>/<int:medical_record_id>/', views.MedicalRecordAPIView.as_view()),
    path('procedure/', views.ProcedureAPIView.as_view()),
    path('procedure-record/<int:procedure_id>/', views.ProcedureRecordAPIView.as_view()),
]