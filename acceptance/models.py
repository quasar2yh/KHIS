from django.db import models
from account.models import Patient, Department
from ocs.models import MedicalRecord, Procedure

# Create your models here.

class Claim(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('cancelled', 'cancelled'),
        ('draft', 'draft'),
        ('entered-in-error', 'entered-in-error'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    grand_total = models.DecimalField(max_digits=11, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

class ProcedureFee(models.Model):
    procedure_id = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=11, decimal_places=2)
    effective_date = models.DateField()

class ChargeItem(models.Model):
    claim_id = models.ForeignKey(Claim, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    total = models.DecimalField(max_digits=11, decimal_places=2)

