from rest_framework import serializers
from .models import Appointment
from account.models import Patient, Practitioner, Department
from datetime import time
from django.utils import timezone
from datetime import time, timedelta as td


class AppointmentSreailizer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'department', 'start',
                  'reason', 'active', 'patient', 'practitioner', 'end', 'minutesDuration', 'appointmentType', 'status']
        read_only_fields = ['patient']

    def validate_datetime(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("예약 일시는 현재 일시보다 이후여야 합니다.")
        if value.minute % 20 != 0:
            raise serializers.ValidationError('예약 시간은 20분 단위로만 가능합니다.')
        if value.second != 0:
            raise serializers.ValidationError('예약 시간의 초는 00초만 가능합니다')
        start_time = time(9, 0)
        end_time = time(17, 40)
        if not (start_time <= value.time() <= end_time):
            raise serializers.ValidationError('예약 시간은 진료시간 내에 있어야 합니다.')

        return value

    def validate(self, data):
        practitioner = data.get('practitioner')
        start = data.get('start')
        patient = self.context.get('patient')
        department = data.get('department')
        appointmentType = data.get('appointmentType')
        minutesDuration = data.get('minutesDuration')

        # appointmentType 따른 minutesDuration 할당
        if appointmentType == 'routine':
            minutesDuration = 10
        elif appointmentType == 'walkin':
            minutesDuration = 10
        elif appointmentType == 'checkup':
            minutesDuration = 40
        elif appointmentType == 'followup':
            minutesDuration = 30
        elif appointmentType == 'emergency':
            minutesDuration = 30
        else:
            minutesDuration = 50
        end = start+td(minutes=minutesDuration)
        if start >= end:
            raise serializers.ValidationError("예상 예약종료시간 보다 이후여야 합니다.")
        data['end'] = end
        data['minutesDuration'] = minutesDuration

        practitioner_appointments = Appointment.objects.filter(
            practitioner=practitioner,
            start=start,
            active=True,
            department=department
        ).exclude(pk=self.instance.pk if self.instance else None)
        patient_appointments = Appointment.objects.filter(
            patient=patient,
            start=start
        ).exclude(pk=self.instance.pk if self.instance else None)

        if patient_appointments.exists():
            raise serializers.ValidationError("환자분은 해당 시간에 다른 예약이 있습니다.")
        if practitioner_appointments.exists():
            raise serializers.ValidationError('해당과의  선생님은 이미 예약이 있습니다.')

        return data


class AppointmentListSerializer(serializers.Serializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False)
    practitioner = serializers.PrimaryKeyRelatedField(
        queryset=Practitioner.objects.all(), required=False)
    datetime = serializers.DateTimeField(required=False)
    date = serializers.DateField(required=False)
    time = serializers.TimeField(required=False)


class PractitionerAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practitioner
        fields = ['id', 'department']
