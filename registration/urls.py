from django.urls import path
from . import views

app_name = 'ocs'
urlpatterns = [
    path('', views.PatientAPIView.as_view()),
    path('<int:patient_id>/', views.PatientAPIView.as_view()),
]