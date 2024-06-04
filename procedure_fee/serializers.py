from rest_framework import serializers
from .models import ProcedureFee


class ProcedureFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureFee
        fields = '__all__'