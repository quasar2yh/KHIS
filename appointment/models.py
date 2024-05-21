from django.db import models
from account.models import Department, Patient, Practitioner
from django.core.exceptions import ValidationError
from datetime import time, timedelta as td
from django.utils import timezone


class Appointment(models.Model):
    # 예약 상태 (예: proposed, pending, booked 등)
    status = models.CharField(null=True, max_length=20, choices=[
        ('proposed', 'Proposed'),
        ('booked', 'Booked'),
        ('pending', 'Pending'),
        ('arrived', 'Arrived'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
        ('noshow', 'No Show'),
        ('entered_in_error', 'Entered in Error'),
        ('waitlist', 'Waitlist'),
    ])
    # 예약 유형
    appointmentType = models.CharField(max_length=20, choices=[
        ('routine', 'Routine'),
        ('walkin', 'Walkin'),
        ('checkup', 'Checkup'),
        ('followup', 'Followup'),
        ('emergency', 'Emergency'),
    ])
    # 예약자
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # 의사
    practitioner = models.ForeignKey(
        Practitioner, on_delete=models.CASCADE, blank=True, null=True)
    # 진료과
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    # 예약 시작 시간
    start = models.DateTimeField()
    # 예상되는 진료 시간
    minutesDuration = models.PositiveSmallIntegerField(
        blank=True, null=True)  # 일단 null Ture 추가
    # 예약 종료 시간
    end = models.DateTimeField(blank=True, null=True)  # 일단 null Ture 추가
    # 요청된 예약 기간
    requested_period_start = models.DateTimeField(null=True, blank=True)
    requested_period_end = models.DateTimeField(null=True, blank=True)
    # 예약에 대한 추가 정보
    description = models.TextField(null=True, blank=True)
    # 예약 사유
    reason = models.TextField(null=True, blank=True)
    # 예약 생성 날짜
    created = models.DateTimeField(auto_now_add=True)
    # 예약 취소 날짜
    cancellation_date = models.DateTimeField(null=True, blank=True)
    # 예약 취소 이유
    cancellation_reason = models.TextField(null=True, blank=True)
    # 환자 지시사항
    patient_instruction = models.TextField(null=True, blank=True)
    # 예약 현황
    active = models.BooleanField()

    def clean(self):
        if self.start <= timezone.now():
            raise ValidationError("예약 일시는 현재 일시보다 이후여야 합니다.")
        if self.start <= self.end:
            raise ValidationError("예상 예약종료시간 보다 이후여야 합니다.")
        if self.start.minute % 20 != 0:
            raise ValidationError('예약 시간은 20분 단위로만 가능합니다.')
        if self.start.second != 0:
            raise ValidationError('예약 시간의 초는 00초만 가능합니다')
        start_time = time(9, 0)
        end_time = time(17, 40)
        if not (start_time <= self.start.time() <= end_time):
            raise ValidationError('예약 시간은 진료시간 내에 있어야 합니다.')
        practitioner_appointments = Appointment.objects.filter(
            practitioner=self.practitioner,
            start=self.start,
            active=True,
            department=self.department
        ).exclude(pk=self.pk)
        patient_appointments = Appointment.objects.filter(
            patient=self.patient,
            start=self.start
        ).exclude(pk=self.pk)

        if patient_appointments.exists():
            raise ValidationError("환자분은 해당 시간에 다른 예약이 있습니다.")
        if practitioner_appointments.exists():
            raise ValidationError('해당과의 선생님은 이미 예약이 있습니다.')

    def save(self, *args, **kwargs):
        # appointmentType에 따라 minutesDuration 설정
        if self.appointmentType == 'routine':
            self.minutesDuration = 10
        elif self.appointmentType == 'walkin':
            self.minutesDuration = 10
        elif self.appointmentType == 'checkup':
            self.minutesDuration = 40
        elif self.appointmentType == 'followup':
            self.minutesDuration = 30
        elif self.appointmentType == 'emergency':
            self.minutesDuration = 30
        else:
            self.minutesDuration = 50
        self.end = self.start+td(minutes=self.minutesDuration)

        self.clean()

        super().save()


class Waiting(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)