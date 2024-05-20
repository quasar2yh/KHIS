from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'appointment'
urlpatterns = [
    path('patient/<int:patient_id>/',
         views.AppointMentAPIView.as_view(), name="appoint"),
]
