from rest_framework import serializers
from .models import Appointment
from account.models import Patient, Practitioner, Department


class AppointmentSreailizer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'department', 'datetime',
                  'syptom', 'active', 'patient', 'practitioner']
        read_only_fields = ['patient', 'practitioner']
