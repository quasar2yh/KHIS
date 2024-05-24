from rest_framework import serializers
from .models import Appointment
from account.models import Patient, Practitioner, Department
from datetime import time
from django.utils import timezone
from datetime import time, timedelta as td




class AppointmentDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'active', 'status',
                  'cancellation_reason', 'cancellation_date',]
        read_only_fields = ['active', 'status', 'patient', 'id']

    def update(self, instance, validated_data):
        instance.active = False
        instance.status = 'cancelled'
        instance.cancellation_reason = validated_data.get(
            'cancellation_reason', instance.cancellation_reason)
        instance.cancellation_date = validated_data.get(
            'cancellation_date', timezone.now())
        instance.save()
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'department', 'start',
                  'reason', 'active', 'patient', 'practitioner', 'end', 'minutesDuration', 'appointmentType', 'status', "created"]
        read_only_fields = ['patient', 'id']

    def create(self, validated_data):
        appointment = Appointment(**validated_data)
        return appointment

    def validate_start(self, value):
        local_value = timezone.localtime(value)
        if local_value <= timezone.now():
            raise serializers.ValidationError("예약 일시는 현재 일시보다 이후여야 합니다.")
        if local_value.minute % 20 != 0:
            raise serializers.ValidationError('예약 시간은 20분 단위로만 가능합니다.')
        if local_value.second != 0:
            raise serializers.ValidationError('예약 시간의 초는 00초만 가능합니다')
        start_time = time(9, 0)
        end_time = time(17, 40)
        if not (start_time <= local_value.time() <= end_time):
            raise serializers.ValidationError('예약 시간은 진료시간 내에 있어야 합니다.')

        return value

    def validate_appointmentType(self, value):
        # Patient가 선택할 수 있는 유형
        allowed_types = ['routine', 'checkup', 'followup']
        # 현재 사용자가 Patient인지 확인
        if self.context.get('subject') == 'Patient':
            if value not in allowed_types:
                # Patient 유형이 제한된 예약 유형을 선택하지 않았을 경우
                raise serializers.ValidationError(
                    "Patient는 Routine, Checkup, Followup 중에서만 선택 가능합니다.")

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
        # start end 비교 검증
        last_appointment = Appointment.objects.filter(
            patient=patient).order_by('-created').first()
        if last_appointment:
            last_appointment_end = last_appointment.end
            last_appointment_end_local = timezone.localtime(
                last_appointment_end)
            if start <= last_appointment_end_local:
                raise serializers.ValidationError(
                    "새로운 예약의 start시간은 직전 예약의 예약종료시간 보다 이후여야 합니다.")

        data['end'] = end
        data['minutesDuration'] = minutesDuration

        return data


class AppointmentListSerializer(serializers.Serializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False)
    practitioner = serializers.PrimaryKeyRelatedField(
        queryset=Practitioner.objects.all(), required=False)
    start = serializers.DateTimeField(required=False)
    date = serializers.DateField(required=False)
    time = serializers.TimeField(required=False)
    practitioner_all = serializers.CharField(required=False)  # 전체의사 조회할때 쓰는 필드


class PractitionerAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practitioner
        fields = ['id', 'department']
