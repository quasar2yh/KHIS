from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'appointment'
urlpatterns = [
    path('patient/<int:patient_id>/',
         views.AppointMentAPIView.as_view(), name="appoint"),
    path('checklist/', views.AppointmentListAPIView.as_view(), name="checklist"),
     path('waiting/', views.WaitingListView.as_view()),
     path('chatbot/', views.AiConsultationView.as_view()),
]
