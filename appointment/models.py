from django.db import models
from account.models import Department, Patient, Practitioner
from django.core.exceptions import ValidationError
from datetime import time


class Appointment(models.Model):
    # 환자의 예약 데이터
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    practitioner = models.ForeignKey(
        Practitioner, on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField()
    syptom = models.TextField()
    # 증상
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField()  # 예약 처리 확인  f - 끝난 예약 t 진행 예약

    def clean(self):
        if self.datetime.minute % 20 != 0:
            raise ValidationError('예약 시간은 20분 단위로만 가능합니다.')
        if self.datetime.second != 0:
            raise ValidationError('예약 시간의 초는 00초만 가능합니다')
        start_time = time(9, 0)
        end_time = time(17, 40)
        if not (start_time <= self.datetime.time() <= end_time):
            raise ValidationError('예약 시간은 진료시간 내에 있어야 합니다.')

        practitioner_appointments = Appointment.objects.filter(
            practitioner=self.practitioner,
            datetime=self.datetime,
            active=True
        ).exclude(pk=self.pk)

        if practitioner_appointments.exists():
            raise ValidationError('해당 선생님은 이미 예약이 있습니다.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save()
