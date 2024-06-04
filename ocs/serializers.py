from rest_framework import serializers
from .models import MedicalRecord, ProcedureRecord, Procedure, ProcedureFee


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'


class ProcedureRecordSerializer(serializers.ModelSerializer):
    procedure = ProcedureSerializer()

    class Meta:
        model = ProcedureRecord
        fields = '__all__'

    def create(self, validated_data):
        procedure_data = validated_data.pop('procedure')
        procedure = Procedure.objects.create(**procedure_data)
        procedure_record = ProcedureRecord.objects.create(
            procedure=procedure, **validated_data)
        return procedure_record

    def update(self, instance, validated_data):
        procedure_data = validated_data.pop('procedure', None)

        if procedure_data:
            procedure_serializer = ProcedureSerializer(
                instance.procedure, data=procedure_data, partial=True)
            if procedure_serializer.is_valid():
                procedure_serializer.save()

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['procedure'] = ProcedureSerializer(instance.procedure).data
        return response

class ProcedureFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureFee
        fields = '__all__'
