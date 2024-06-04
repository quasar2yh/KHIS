from django.urls import path
from . import views

urlpatterns = [
    path('', views.MedicalRecordAPIView.as_view()),
    path('<int:patient_id>/', views.MedicalRecordAPIView.as_view()),
    path('<int:patient_id>/<int:medical_record_id>/', views.MedicalRecordAPIView.as_view()),
    path('procedure/', views.ProcedureAPIView.as_view()),
    path('procedure/<int:procedure_id>', views.ProcedureDetailAPIView.as_view()),
    path('ProcedureFee/', views.ProcedureFeeAPIView.as_view()),
    path('ProcedureFee/<int:procedurefee_id>', views.ProcedureFeeDetailAPIView.as_view()),
    path('procedure-record/', views.ProcedureRecordAPIView.as_view()),
    path('procedure-record/<int:procedure_record_id>/', views.ProcedureRecordAPIView.as_view()),
    path('procedure-record-list/<int:medical_record_id>/', views.ProcedureRecordListAPIView.as_view()),
]