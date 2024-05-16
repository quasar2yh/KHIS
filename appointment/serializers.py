from rest_framework import serializers
from .models import Appointment
from account import Patient, Practitioner, Department


class AppointmentSreailizer(serializers.ModelSerializer):
        class Meta:
            model = Appointment
            fields = ['id', 'department', 'datetime',
                'syptom', 'active']
            read_only_fields = ['patient','practitioner']
            
        
