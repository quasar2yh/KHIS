from django.db import models
from account.models import Patient, Practitioner, Department
from acceptance.models import ChargeItem
from procedure.models import Procedure

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    practitioner = models.ForeignKey(Practitioner, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    # 진단 내용
    diagnosis = models.TextField()
    # 진단 결과
    diagnostic_results = models.TextField(blank=True)
    # 수술 요청 기록
    surgical_request_record = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 수술 기록
class ProcedureRecord(models.Model):
    # 수술, 환자, 의료진, 진료기록 FK
    procedure = models.ForeignKey(Procedure, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    practitioner = models.ForeignKey(Practitioner, on_delete=models.PROTECT)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.PROTECT)
    # 수술 결과
    procedure_result = models.TextField()
    # 수술 시간
    start = models.DateTimeField()
    end = models.DateTimeField()
    charge_item = models.OneToOneField(
        ChargeItem, on_delete=models.PROTECT, blank=True, null=True)

