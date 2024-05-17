from django.contrib import admin
from django.urls import path
from .views import MedicalScheduleAPIView




app_name = 'schedule'
urlpatterns = [
    
    path("medical/", MedicalScheduleAPIView.as_view(), name="medical_list"), # 연차 신청 및 조회
#     path("medical/<int:medical_id>/", MedicalScheduleDetailAPIView.as_view(), name="medical_detail"),  # 본인 연차 상세 조회 수정 및 삭제
#     # path("hospital/<int:medical_id>/", .as_view(), name="medical_detail"),
#     # path("hospital/{staff_id}/", .as_view(), name="medical_detail"),
    
]





