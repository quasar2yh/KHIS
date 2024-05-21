from django.contrib import admin
from django.urls import path
from .views import (
     MedicalScheduleAPIView,
     SpecificScheduleAPIView, 
     HospitalScheduleAPIView,
     HospitalScheduleDetailAPIView,
     IntegratedScheduleAPIView,
     MedicalIntegratedAPIView,
     MedicalSpecificIntegratedAPIView,
     
     )


app_name = 'schedule'
urlpatterns = [

    path("medical/", MedicalScheduleAPIView.as_view(),
         name="medical_holiday"),  # 연차 신청 및 본인 연차 조회
    
    path("medical/specific/", SpecificScheduleAPIView.as_view(),
         name="medical_specific_holiday"),  # 특정 구간 본인 연차 조회
    
    
    path("medical/integration/", MedicalIntegratedAPIView.as_view(),
         name="medical_integrated_holiday"),  # 전체 직원 연차 조회
    
    
     path("medical/specific/integration/", MedicalSpecificIntegratedAPIView.as_view(),
         name="medical_specific_integrated_holiday"),  # 전체 직원 연차의 구간 조회
    

    path('hospital/', HospitalScheduleAPIView.as_view(),
         name='hospital_holiday'),  # 공휴일 포함 병원 휴일 등록 및 조회

    path("hospital/<int:hospitalschedule_id>/", HospitalScheduleDetailAPIView.as_view(),
         name="hospital_detail_holiday"),  # 병원 휴일 수정 및 삭제
    

     path("integration/", IntegratedScheduleAPIView.as_view(), name="integrated_holiday"), # 의료진 휴무 포함 병원 전체 일정 조회
     
     
]