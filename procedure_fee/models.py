from django.db import models
from procedure.models import Procedure 

class ProcedureFee(models.Model):
    procedure = models.ForeignKey(
        Procedure, on_delete=models.PROTECT, related_name='procedure_fee')
    fee = models.DecimalField(max_digits=11, decimal_places=2)
    effective_start = models.DateField()
    effective_end = models.DateField()
    updated = models.DateTimeField(auto_now=True)