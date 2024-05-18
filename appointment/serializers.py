from rest_framework import serializers
from .models import Appointment
from account.models import Patient, Practitioner, Department
from datetime import time


class AppointmentSreailizer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'department', 'datetime',
                  'syptom', 'active', 'patient', 'practitioner']
        read_only_fields = ['patient']

    def validate_datetime(self, value):
        if value.minute % 20 != 0:
            raise serializers.ValidationError('예약 시간은 20분 단위로만 가능합니다.')
        # if Appointment.objects.filter(datetime=value).exists():
        #     raise serializers.ValidationError("이미 예약된 시간 입니다")
        if value.second != 0:
            raise serializers.ValidationError('예약 시간의 초는 00초만 가능합니다')
        start_time = time(9, 0)
        end_time = time(17, 40)
        if not (start_time <= value.time() <= end_time):
            raise serializers.ValidationError('예약 시간은 진료시간 내에 있어야 합니다.')

        return value

    def validate(self, data):
        practitioner = data.get('practitioner')
        datetime = data.get('datetime')

        practitioner_appointments = Appointment.objects.filter(
            practitioner=practitioner,
            datetime=datetime,
            active=True
        ).exclude(pk=self.instance.pk if self.instance else None)
        if practitioner_appointments.exists():
            raise serializers.ValidationError('해당 선생님은 이미 예약이 있습니다.')
        return data
