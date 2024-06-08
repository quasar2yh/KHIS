from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientAPIView.as_view()),
    path('<int:patient_id>/', views.PatientAPIView.as_view()),
    path('related-person/<int:patient_id>/', views.RelatedPersonAPIView.as_view()),
    path('related-person/<int:patient_id>/<int:related_person_id>/', views.RelatedPersonAPIView.as_view()),
    path('search/', views.PatientSearchAPIView.as_view()),
]