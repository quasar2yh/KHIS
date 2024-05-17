from django.db import models
from account.models import Department, Patient, Practitioner


class Appointment(models.Model):
    # 환자의 예약 데이터
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    practitioner = models.ForeignKey(
        Practitioner, on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField()
    syptom = models.TextField()
    # 증상
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField()  # 예약 처리 확인  f - 끝난 예약 t 진행 예약
