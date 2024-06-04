from django.db import models


class Claim(models.Model):
    STATUS_CHOICES = [
        ('complete', 'complete'),
        ('active', 'active'),
        ('cancelled', 'cancelled'),
        ('draft', 'draft'),
        ('entered-in-error', 'entered-in-error'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    grand_total = models.DecimalField(max_digits=11, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)


class ChargeItem(models.Model):
    claim_id = models.ForeignKey(
        Claim, on_delete=models.CASCADE, related_name="chargeItem")
    quantity = models.PositiveSmallIntegerField()
    total = models.DecimalField(max_digits=11, decimal_places=2)
