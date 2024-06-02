from rest_framework import serializers
from .models import MedicalRecord, ProcedureRecord, Procedure


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'


class ProcedureRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcedureRecord
        fields = '__all__'