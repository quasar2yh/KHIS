from django.db import models
from account.models import Practitioner, Practitioner
from account.models import Department


from django.dispatch import receiver
from django.db.models.signals import post_save


#의료진이 생성될 때마다 연차 정보를 자동으로 생성하도록 설정
@receiver(post_save, sender=Practitioner)
def create_annual_leave(sender, instance, created, **kwargs):
    if created:
        AnnualLeave.objects.create(practitioner=instance)


# 의료진 연차 스케줄

class Annual(models.Model):
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)

    # 연차 사용한 날짜 (시작,끝)
    start_date = models.DateField(db_column='start_date')
    end_date = models.DateField(db_column='end_date')

    # 연차 사유
    reason = models.TextField()

    def __str__(self):
        return f"{self.practitioner} - {self.start_date} ~ {self.end_date}"

 # 병원 전체 휴일


class HospitalSchedule(models.Model):

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


# 연차 소진일
class AnnualLeave(models.Model):
    practitioner = models.OneToOneField(Practitioner, on_delete=models.CASCADE)
    annual_leave_count = models.IntegerField(default=15)  # 매년 15일 연차 지급
    leave_taken = models.IntegerField(default=0)  # 사용한 연차 수

    def remaining_leave(self):
        return self.annual_leave_count - self.leave_taken

    def __str__(self):
        return f"{self.practitioner} - Remaining Leave: {self.remaining_leave()}"
    

