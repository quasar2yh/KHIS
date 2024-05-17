from django.db import models
from account.models import Patient

# Create your models here.
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    # 진단 내용
    diagnostic_results = models.TextField(blank=True)
    # 진단 결과
    surgical_request_record = models.TextField(blank=True)
    # 수술 요청 기록
    surgical_result = models.TextField(blank=True)
    # 수술 결과
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

