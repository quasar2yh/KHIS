# schedule/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import DepartmentEvent, Practitioner
from django.core.mail import send_mail
from account.models import Department, HumanName
from django.core.exceptions import ObjectDoesNotExist


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
        print("이메일이 성공적으로 발송되었습니다.")
        return {"success": "메일이 성공적으로 발송되었습니다"}
    except Exception as e:
        print("이메일 발송 중 오류 발생:", str(e))
        return {"error": str(e)}


@shared_task
def send_department_event_reminder():

    now = timezone.localtime()
    start_time = now + timedelta(hours=1)
    end_time = now + timedelta(hours=2)

    print(f"\n\n\n시간체크!\n\n")
    print(f"현재 시간: {now}")
    print(f"시작 시간: {start_time}, 종료 시간: {end_time}")

    departments = Department.objects.all()
    for department in departments:
        events = DepartmentEvent.objects.filter(
            department=department,
            start_time__range=(start_time, end_time)
        )

    print(f"\n\n\n이벤트 가져오기! :", events)

    for event in events:
        print("이벤트:", event)

        if event.department:
            practitioners = Practitioner.objects.filter(
                department=event.department)
            print("관련 의료진:", practitioners)
            for practitioner in practitioners:
                human_name = HumanName.objects.get(practitioner=practitioner)
                practitioner_name = f"{human_name.family}{human_name.name}"
                subject = f"부서 일정 알람: {event.event_title}"
                message = (
                    f"안녕하세요 {practitioner_name} 선생님,\n\n"
                    f"곧 다음 일정이 예정되어 있습니다:\n\n"
                    f"제목: {event.event_title}\n"
                    f"내용: {event.event_content}\n"
                    f"시작 시간: {event.start_time}\n"
                    f"종료 시간: {event.end_time}\n\n"
                    f"감사합니다,\nKHIS병원"
                )
                sender_email = 'ritsukoice@naver.com'
                send_email_async.delay(
                    subject, message, sender_email, practitioner.account.email)
        else:
            print("이벤트에 부서 정보가 없습니다.")
