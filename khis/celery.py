from celery import Celery
import os

# Django 설정 모듈을 Celery 애플리케이션의 설정으로 사용
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khis.settings')

# Celery 애플리케이션 생성
app = Celery('khis')

# Django 설정 모듈을 Celery 애플리케이션의 설정으로 사용
app.config_from_object('django.conf:settings', namespace='CELERY')

# 등록할 작업 모듈의 위치를 지정
app.autodiscover_tasks()

# Celery Beat 설정 추가
app.conf.beat_schedule = {
    'send-department-event-reminder-every-hour': {
        'task': 'schedule.tasks.send_department_event_reminder',  # 실행할 작업
        'schedule': 3600,  # 스케줄(초 단위). 여기서는 1시간마다 실행
    },
}
