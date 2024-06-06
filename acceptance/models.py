from django.db import models
from account.models import Patient
from procedure.models import Procedure


class Claim(models.Model):
    STATUS_CHOICES = [
        ('complete', 'complete'),
        ('active', 'active'),
        ('cancelled', 'cancelled'),
        ('draft', 'draft'),
        ('entered-in-error', 'entered-in-error'),
    ]
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="claims")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    grand_total = models.DecimalField(
        max_digits=11, decimal_places=2, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ChargeItem(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="charge_items")
    claim = models.ForeignKey(
        Claim, on_delete=models.CASCADE, related_name="charge_items")
    procedure = models.OneToOneField(
        Procedure, on_delete=models.PROTECT, related_name="charge_items")
    quantity = models.PositiveSmallIntegerField()
    total = models.DecimalField(max_digits=11, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
