from django.db import models
from account.models import Department, Practitioner, Practitioner
# Create your models here.


class Schedule(models.Model):
    # 병원 쪽 스케줄
    # ex) 병원 휴일, 해당 의사 연차, ...
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    practitioner = models.ForeignKey(
        Practitioner, on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField()


class Annual(models.Model):
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)

    # 연차 사용한 날짜 (시작,끝)
    start_date = models.DateField(db_column='start_date')
    end_date = models.DateField(db_column='end_date')

    # 연차 사유
    reason = models.TextField()

    def __str__(self):
        return f"{self.practitioner} - {self.start_date} ~ {self.end_date}"
