# schedule/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta  # 
from .models import DepartmentEvent, Practitioner
from django.core.mail import send_mail

@shared_task
def send_email_async(subject, message, sender_email, recipient_email):
    try:
        send_mail(
            subject,
            message,
            sender_email,
            [recipient_email],
            fail_silently=False,
        )
        return {"success": "메일이 성공적으로 발송되었습니다"}
    except Exception as e:
        return {"error": str(e)}



@shared_task
def send_department_event_reminder(): # 부서별 일정 알람
    now = timezone.now()
    # 현재시간 1시간 후의 시간 계산
    start_time = now + timedelta(hours=1)
    # 현재시간 2시간 후의 시간 계산
    end_time = now + timedelta(hours=2)

    # 이벤트 시작 시간이 start_time과 end_time 사이인 이벤트들 필터링
    events = DepartmentEvent.objects.filter(start_time__range=(start_time, end_time))

    # 각 이벤트에 대해 처리
    for event in events:
        # 이벤트가 속한 부서의 의료진들 조회
        practitioners = Practitioner.objects.filter(department_id=event.department.id)
        # 각 의료진에게 이메일 발송
        for practitioner in practitioners:
            # 이메일 제목 생성
            subject = f"부서 일정 알람: {event.event_title}"
            # 이메일 내용 생성
            message = f"안녕하세요 {practitioner.humanname.family} {practitioner.humanname.name} 선생님,\n\n 곧 다음 일정이 예정되어 있습니다 :\n\n제목: {event.event_title}\n내용: {event.event_content}\n시작 시간: {event.start_time}\n종료 시간: {event.end_time}\n\n감사합니다,\nKHIS병원"
            # 의료진의 이메일 주소
            recipient_email = practitioner.user.email
            # 발신자 이메일 주소
            sender_email = 'ritsukoice@naver.com'
            # 비동기적으로 이메일 발송 작업 실행
            send_email_async.delay(subject, message, sender_email, recipient_email)