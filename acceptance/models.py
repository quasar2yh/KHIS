from django.db import models
from account.models import Patient, Department
from ocs.models import MedicalRecord

# Create your models here.


class Claim(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('cancelled', 'cancelled'),
        ('draft', 'draft'),
        ('entered-in-error', 'entered-in-error'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    insurance = models.CharField(max_length=20)
    patient_paid = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
