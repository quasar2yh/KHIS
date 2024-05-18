from rest_framework import serializers
from .models import Appointment
from account.models import Patient, Practitioner, Department


class AppointmentSreailizer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'department', 'datetime',
                  'syptom', 'active', 'patient', 'practitioner']
        read_only_fields = ['patient', 'practitioner']

    def validate_datetime(self, value):
        if value.minute % 20 != 0:
            raise serializers.ValidationError('예약 시간은 20분 단위로만 가능합니다.')
        return value
