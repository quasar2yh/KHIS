from django.contrib import admin
from django.urls import path
from .views import SchedulelistAPIView,ScheduleDetailAPIView

urlpatterns = [
    
    path("medical/", SchedulelistAPIView.as_view(), name="medical"),
    path("medical/<int:medical_id>/", ScheduleDetailAPIView.as_view(), name="medical"),
    
]

#연차신청
#연차조회 + 연차 기간 조회




