from rest_framework import serializers
from .models import Procedure
from procedure_fee.serializers import ProcedureFeeSerializer

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'


class ProcedureDetailSerializer(serializers.ModelSerializer):
    procedure_fee = ProcedureFeeSerializer(many=True, read_only=True)
    class Meta:
        model = Procedure
        fields = '__all__'