from django.contrib import admin
from django.urls import path
from .views import MedicalScheduleAPIView, SpecificScheduleAPIView,HolidayListAPIView


app_name = 'schedule'
urlpatterns = [

    path("medical/", MedicalScheduleAPIView.as_view(),
         name="medical"),  # 연차 신청 및 조회
    path("medical/specific", SpecificScheduleAPIView.as_view(),
         name="medical-specific"),  # 특정 구간 연차 조회
#     path('holidays/', HolidayListAPIView.as_view(), name='holiday-list'), # 공휴일 조회

    # #     # path("hospital/<int:medical_id>/", .as_view(), name="medical_detail"),
    # #     # path("hospital/{staff_id}/", .as_view(), name="medical_detail"),

]
