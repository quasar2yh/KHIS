from django.db import models
from account.models import Patient, Practitioner, Department
from acceptance.models import ChargeItem


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


# 수술
class Procedure(models.Model):
    # 수술 코드
    procedure_code = models.CharField(max_length=30)
    # 수술 이름
    procedure_name = models.CharField(max_length=30)
    # 상세 설명
    description = models.TextField()


# 수술 기록
class ProcedureRecord(models.Model):
    # 수술, 환자, 의료진, 진료기록 FK
    procedure = models.ForeignKey(Procedure, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    practitioner = models.ForeignKey(Practitioner, on_delete=models.PROTECT)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.PROTECT)
    # 수술 결과
    procedure_result = models.TextField(blank=True, null=True)
    # 수술 시간
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    charge_item = models.ForeignKey(ChargeItem, on_delete=models.PROTECT, blank=True, null=True)


class ProcedureFee(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=11, decimal_places=2)
    effective_date = models.DateField()