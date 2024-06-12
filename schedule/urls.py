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
    HospitalPublicScheduleAPIView,
    DepartmentListAPIView,
    DepartmentMedicalScheduleAPIView,
    MailAPIView,
    DepartmentRegisterAPIView,
    DepartmentPractitionerAPIView,
    DepartmentEventAPIView,
    DepartmentEventDetailAPIView,
    DepartmentMedicalSpecificScheduleAPIView,
    AnnualLeaveStatusAPIView,
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
         name='hospital_holiday'),  # 병원 자체 휴일 등록 및 조회


    path("hospital/<int:hospitalschedule_id>/", HospitalScheduleDetailAPIView.as_view(),
         name="hospital_detail_holiday"),  # 병원 자체 휴일 수정 및 삭제

    path('hospital/public/', HospitalPublicScheduleAPIView.as_view(),
         name='hospital_public_holiday'),  # 국가 공휴일 조회

    path("integration/", IntegratedScheduleAPIView.as_view(),
         name="integrated_holiday"),  # 병원 + 의료진 전체 일정 조회


    path("department-Register/", DepartmentRegisterAPIView.as_view(),
         name="department_list"),  # 부서 등록

    path("department/", DepartmentListAPIView.as_view(),
         name="department_list"),  # 부서 조회

    path("department/<int:department_id>/holiday/", DepartmentMedicalScheduleAPIView.as_view(),
         name="department_medical_holiday"),  # 부서별 의료진 연차 조회

    path("department/<int:department_id>/specific/holiday/", DepartmentMedicalSpecificScheduleAPIView.as_view(),
         name="department_medical_specific_holiday"),  # 부서별 의료진 연차 구간조회


    path("department/<int:department_id>/practitioner/", DepartmentPractitionerAPIView.as_view(),
         name="department_practitioner"),  # 부서별 의료진 조회


    path("department/<int:department_id>/event/", DepartmentEventAPIView.as_view(),
         name="department_event"),  # 부서별 일정 등록

    path("department/<int:department_id>/event/<int:event_id>/", DepartmentEventDetailAPIView.as_view(),
         name="department_event_detail"),  # 부서별 일정 수정 및 삭제


    path('send_email/', MailAPIView.as_view(), name='send_email'),  # 메일 보내기


    path("medical/annual-leave/", AnnualLeaveStatusAPIView.as_view(),
         name="medical_annual_leave"),  # 본인 연차 소진일 조회

    path("medical/annual-leave/", AnnualLeaveStatusAPIView.as_view(),
         name="medical_annual_leave"),  # 연차 소진일 조회





]
