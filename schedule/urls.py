from django.contrib import admin
from django.urls import path
from .views import ScheduleListAPIView, ScheduleDetailAPIView

urlpatterns = [
    
    path("medical/", ScheduleListAPIView.as_view(), name="medical_list"),
    path("medical/<int:medical_id>/", ScheduleDetailAPIView.as_view(), name="medical_detail"),
    
]

#연차신청
#연차조회 + 연차 기간 조회




