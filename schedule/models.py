from django.db import models
from account.models import Practitioner, Practitioner
from account.models import Department

# Create your models here.


class Annual(models.Model):  # 의료진 연차 스케줄
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)

    # 연차 사용한 날짜 (시작,끝)
    start_date = models.DateField(db_column='start_date')
    end_date = models.DateField(db_column='end_date')

    # 연차 사유
    reason = models.TextField()

    def __str__(self):
        return f"{self.practitioner} - {self.start_date} ~ {self.end_date}"


class HospitalSchedule(models.Model):      # 병원 전체 휴일

    date = models.DateField()
    date_name = models.CharField(max_length=255)
    is_public_holiday = models.BooleanField(default=False)  # 공휴일 여부
    is_hospital_holiday = models.BooleanField(default=False)  # 병원 자체 휴일 여부

    def __str__(self):
        return f"{self.date} - {self.description}"


# 부서별 일정
class DepartmentEvent(models.Model):
    department = models.ForeignKey(
        'account.Department', on_delete=models.CASCADE, db_column='department_id')
    event_title = models.CharField(max_length=255, db_column='event_title')
    event_content = models.TextField(
        blank=True, null=True, db_column='event_content')
    start_time = models.DateTimeField(db_column='start_time')
    end_time = models.DateTimeField(db_column='end_time')

    def __str__(self):
        return f"{self.event_title} - {self.start_time} ~ {self.end_time}"
