from django.db import models
from account.models import Department, Practitioner, Practitioner

# Create your models here.



class Annual(models.Model): # 의료진 연차 스케줄 
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)

    # 연차 사용한 날짜 (시작,끝)
    start_date = models.DateField(db_column='start_date')
    end_date = models.DateField(db_column='end_date')

    # 연차 사유
    reason = models.TextField()

    def __str__(self):
        return f"{self.practitioner} - {self.start_date} ~ {self.end_date}"


class HospitalSchedule(models.Model):      # 병원 공휴일 관리

    date = models.DateField()
    date_name = models.CharField(max_length=255)
    is_holiday = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} - {self.description}"
    
    
    
