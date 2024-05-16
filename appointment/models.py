from django.db import models
from account.models import Department, Patient, Practitioner


class Appointment():
    # 환자의 예약 데이터
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    practitioner = models.ForeignKey(Practitioner,on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField()
    syptom = models.TextField()
    # 증상
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    active = models.BooleanField()