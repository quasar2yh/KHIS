
from django.utils import timezone
from .open_ai import chatgpt
from .models import Appointment, Practitioner, Department
from datetime import datetime, timedelta, time as dt_time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import AppointmentSerializer, AppointmentListSerializer, AppointmentScheduleSerializer, PractitionerAppointmentSerializer, AppointmentDelSerializer, HospitalScheduleSerializer, AnnualSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import Patient
from django.contrib.auth.hashers import check_password
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import AllowAny
from django.utils.dateparse import parse_datetime, parse_time, parse_date
from schedule.models import Annual, HospitalSchedule, DepartmentEvent
from datetime import datetime
from django.db.models import Q
import boto3


class AppointMentAPIView(APIView):  # 예약기능 CRUD
    permission_classes = [IsAuthenticated]

    def get_patient(self, patient_id):

        return get_object_or_404(Patient, pk=patient_id)
    # 부서별 휴일

    def get_hospital_holidays(self):  # 병원 휴일 조회
        today = datetime.now().date()
        thirty_days_later = today + timedelta(days=30)
        hospital_holidays = HospitalSchedule.objects.filter(
            date__range=[today, thirty_days_later],
            is_hospital_holiday=True
        ).values_list('date', flat=True) | HospitalSchedule.objects.filter(
            date__range=[today, thirty_days_later],
            is_public_holiday=True
        ).values_list('date', flat=True)
        holidays = set(hospital_holidays)
        return holidays

    def post(self, request, patient_id):
        patient = self.get_patient(patient_id)
        subject = request.user.subject
        data = request.data
        practitioner = data.get('practitioner')
        datetime = parse_datetime(data.get('start'))
        department = data.get('department')
        select_date = datetime.date()
        print(practitioner, department, datetime, select_date,
              "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # 부서와 의사 검증
        try:
            practitioners = Practitioner.objects.get(
                id=practitioner, department=department)
        except Exception as e:
            return Response(f"{e}부서와 의사를 확인 해 주세요 ", status=status.HTTP_400_BAD_REQUEST)
        # 연차검증
        annuals = Annual.objects.filter(
            practitioner_id=practitioner, start_date__lte=select_date, end_date__gte=select_date)
        # 병원 공휴일
        holidays = self.get_hospital_holidays()
        if select_date in holidays:
            return Response(f"{select_date}일은 병원의 휴일입니다")
        # 해당의사 연차
        date_in_annuals = annuals.exists()
        if date_in_annuals:
            return Response(f"{select_date}일은 {practitioner}의사의 연차일 입니다")
        # 부서 이벤트
        department_event = DepartmentEvent.objects.filter(
            start_time__date__lte=select_date, end_time__date__gte=select_date, department=department)
        if department_event:
            return Response("해당 의사는 부서 이벤트로 인해 예약 불가 ")

        serializer = AppointmentSerializer(
            data=request.data, context={'patient': patient, 'subject': subject})
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            appointment = Appointment(**validated_data)
            appointment.patient = patient
            appointment.appointment_clean_and_save = True
            appointment.save()
            appointment.appointment_clean_and_save = False
            print(patient.telecom.value, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            phone_number = patient.telecom.value
            # 하이픈 제거
            phone_number = phone_number.replace('-', '')
            # 국제 전화번호 형식으로 변환
            international_number = self.convert_to_international(phone_number)
            print(international_number,
                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # SMS 보내기
            try:
                sms_response = self.send_sms(
                    international_number, "안녕하세요, 예약이 완료되었습니다.")
                print(sms_response, "SMS response")
            except Exception as e:
                print(e, "문자 발송 실패")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_sms(self, phone_number, message):
        sns_client = boto3.client('sns', region_name='ap-northeast-1')
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=message,
        )
        return response

    def convert_to_international(self, phone_number):
        # 대한민국 국제 전화번호 형식 +82
        if phone_number.startswith('010'):
            return '+82' + phone_number[1:]
        else:
            raise ValueError('전화번호 형식이 올바르지 않습니다.')

    def get(self, request, patient_id):
        patient = self.get_patient(patient_id)
        practitioner = request.query_params.get('practitioner')
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        appointments = Appointment.objects.filter(
            patient=patient).order_by('-created')
        if not patient:
            return Response("환자 정보가 없습니다.")
        if start and end:
            start_date = parse_date(start)
            end_date = parse_date(end)
            max_end = start_date + timedelta(days=365)
            if end_date > max_end:
                return Response("조회 시작일로 최대 1년까지만 조회 가능합니다.")
        if start:  # 조회 시작날자로 조회
            start_date = parse_datetime(start)
            if start_date:
                appointments = appointments.filter(start__gte=start_date)

        if end:
            end_date = parse_datetime(end)
            if end_date:
                end_date = end_date + timedelta(days=1)
                appointments = appointments.filter(end__lte=end_date)

        if practitioner:
            appointments = appointments.filter(practitioner=practitioner)

        serializer = AppointmentSerializer(appointments, many=True)

        return Response(serializer.data)

    def delete(self, request, patient_id):
        patient = self.get_patient(patient_id)
        account = patient.account
        start = request.data.get('start')
        password = request.data.get('password')
        appointment = Appointment.objects.get(
            patient=patient, start=start)
        if not appointment.active:
            return Response("이미 취소된 예약 ")
        if check_password(password, account.password):
            serializer = AppointmentDelSerializer(
                appointment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"detail": "예약이 취소되었습니다.", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response("응~비번 틀림~", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, patient_id):
        patient = self.get_patient(patient_id)
        restart = request.data.get('restart')  # 기존예약 시간
        data = request.data
        practitioner = data.get('practitioner')
        datetime = parse_datetime(data.get('start'))
        department = data.get('department')
        select_date = datetime.date()
        print(practitioner, department, datetime, select_date,
              "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # 부서와 의사 검증
        try:
            practitioners = Practitioner.objects.get(
                id=practitioner, department=department)
        except Exception as e:
            return Response(f"{e}부서와 의사를 확인 해 주세요 ", status=status.HTTP_400_BAD_REQUEST)
        # 연차검증
        annuals = Annual.objects.filter(
            practitioner_id=practitioner, start_date__lte=select_date, end_date__gte=select_date)
        # 병원 공휴일
        holidays = self.get_hospital_holidays()
        if select_date in holidays:
            return Response(f"{select_date}일은 병원의 휴일입니다")
        # 해당의사 연차
        date_in_annuals = annuals.exists()
        if date_in_annuals:
            return Response(f"{select_date}일은 {practitioner}의사의 연차일 입니다")
        # 부서 이벤트
        department_event = DepartmentEvent.objects.filter(
            start_time__date__lte=select_date, end_time__date__gte=select_date, department=department)
        if department_event:
            return Response("해당 의사는 부서 이벤트로 인해 예약 불가 ")
        appointment = get_object_or_404(
            Appointment, patient=patient, start=restart)
        account = patient.account
        login_id = request.user.id
        if account.id == login_id:
            serializer = AppointmentSerializer(
                appointment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AppointmentListAPIView(APIView):

    def post(self, request):
        serializer = AppointmentListSerializer(data=request.data)

        if serializer.is_valid():
            department = serializer.validated_data.get('department')
            practitioner = serializer.validated_data.get('practitioner')
            start = serializer.validated_data.get('start')
            practitioner_all = serializer.validated_data.get(
                'practitioner_all')
            # date = serializer.validated_data.get('date')
            # time = serializer.validated_data.get('time')
            # if not time:
            #     return Response("시간을 선택하세요")
            # datetime = dt.combine(date, time)
            query = Appointment.objects.filter(active=True)
            if department:
                query = query.filter(department=department)
            if practitioner:
                query = query.filter(practitioner=practitioner)
            if start:
                query = query.filter(start=start)
            if not start and not practitioner:  # 일시와 진료과만 들어 왔을때

                if practitioner_all:
                    departments_all = Practitioner.objects.all()
                    all_serializer = PractitionerAppointmentSerializer(
                        departments_all, many=True)
                    return Response({
                        "message": "전체 의사",
                        "data": all_serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    departments = Department.objects.get(id=department.id)
                    departments_practitioner = Department.objects.filter(
                        department=departments.department)
                    val_department = PractitionerAppointmentSerializer(
                        departments_practitioner, many=True)
                    return Response({
                        "message": "해당과의 의사",
                        "data": val_department.data
                    }, status=status.HTTP_200_OK)

            if not practitioner and start:  # 시간만 조회
                # 예약된 시간대에 대한 쿼리 준비
                booked_appointments = Appointment.objects.filter(
                    start=start, active=True)
                # 예약된 의사 ID 가져오기
                booked_practitioner_ids = booked_appointments.values_list(
                    'practitioner_id', flat=True)
                # 예약이 가능한 의사 목록 조회
                available_practitioners = Practitioner.objects.exclude(
                    id__in=booked_practitioner_ids)
                if department:
                    available_practitioners = available_practitioners.filter(
                        department=department)

                # 예약 가능한 의사 목록 직렬화
                available_practitioners_serializer = PractitionerAppointmentSerializer(
                    available_practitioners, many=True)

                return Response({
                    "message": "예약가능한 의사",
                    "data": available_practitioners_serializer.data
                }, status=status.HTTP_200_OK)
            if query.exists():  # 시간, 의사 , 부서 조회
                return Response("detail: 해당 조건에 예약이 이미 있습니다.",
                                status=status.HTTP_200_OK)
            else:
                return Response("detail: 예약이 가능합니다.",
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_hospital_holidays(self):  # 병원 휴일 조회
        today = datetime.now().date()
        thirty_days_later = today + timedelta(days=30)
        hospital_holidays = HospitalSchedule.objects.filter(
            date__range=[today, thirty_days_later],
            is_hospital_holiday=True
        ).values_list('date', flat=True) | HospitalSchedule.objects.filter(
            date__range=[today, thirty_days_later],
            is_public_holiday=True
        ).values_list('date', flat=True)
        holidays = set(hospital_holidays)
        return holidays

    def get(self, request):  # 예약 가능 조회
        department = request.query_params.get('department')
        date = request.query_params.get('date')
        time = request.query_params.get('time')
        practitioner = request.query_params.get('practitioner')
        if date:
            date = parse_date(date)
            holidays = self.get_hospital_holidays()
            today = timezone.now().date()
            if date in holidays:
                return Response({f"{date}는 병원의 휴일입니다.get"}, status=status.HTTP_200_OK)
            if date < today:
                return Response("예약일은 현재보다 앞이여아 함다")
        if time:
            time = parse_time(time)
            if not (dt_time(9, 0) <= time <= dt_time(18, 0)):
                return Response({"예약 가능한 시간은 09:00부터 18:00까지입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 일만 선택->해당 날짜에 예약 가능한 의사 목록
        if date and not (time or department or practitioner):
            # 쉬는 의사 조회
            practitioner = Annual.objects.filter(
                start_date__lte=date, end_date__gte=date).values_list('practitioner_id', flat=True)

            # 부서 이벤트 있는지 확인
            departments_event = DepartmentEvent.objects.filter(
                start_time__date__lte=date, end_time__date__gte=date).values_list('department_id', flat=True)
            # 쉬는 의사를 제외한 나머지 의사 조회
            available_practitioners = Practitioner.objects.exclude(
                id__in=practitioner).exclude(department__in=departments_event)

            practitionerserializer = PractitionerAppointmentSerializer(
                available_practitioners, many=True)

            return Response(practitionerserializer.data, status=status.HTTP_200_OK)
        elif time and not (date or department or practitioner):  # 시간만 선택 해당시간에 예약 가능한 의사
            today = timezone.now().date()
            thirty_days_later = today + timedelta(days=30)
            # 모든 의사 조회
            all_practitioners = Practitioner.objects.all().values_list('id', flat=True)
            print("모든 의사:", all_practitioners)
            # 부서 이벤트 있는지 확인
            departments_event = DepartmentEvent.objects.filter(
                Q(start_time__date__lte=thirty_days_later, end_time__date__gte=today) & Q(end_time__date__gt=today)) .values_list('department_id', flat=True)
            # 30일 안으로 연차 있는 의사 조회
            resting_practitioners = Annual.objects.filter(
                start_date__lte=thirty_days_later, end_date__gte=today
            ).values_list('practitioner_id', flat=True)
            print("연차 중인 의사:", resting_practitioners)

            # 연차가 끝나는 날이 오늘 이후인 의사 포함
            available_practitioners_ids = Practitioner.objects.filter(
                Q(id__in=resting_practitioners) | Q(
                    id__in=all_practitioners) & Q(annual__end_date__gt=today)
            ).values_list('id', flat=True)
            print("사용 가능한 의사 ID:", available_practitioners_ids)

            # 해당 시간에 예약이 있는 의사 조회
            booked_practitioners = Appointment.objects.filter(
                start__date__range=[today, thirty_days_later],
                start__time=time
            ).values_list('practitioner_id', flat=True)
            print("예약이 있는 의사:", booked_practitioners)

            # 예약이 있는 의사 중 해당 기간 내에 예약이 비어있는 의사 포함
            appointment_available_practitioners = Practitioner.objects.filter(
                Q(id__in=booked_practitioners) | Q(id__in=all_practitioners)
            )
            print("예약 가능 의사:", appointment_available_practitioners)

            # 최종 이용 가능한 의사 조회
            final_available_practitioners = Practitioner.objects.filter(
                id__in=appointment_available_practitioners
            ).filter(
                id__in=available_practitioners_ids
            ).exclude(department__in=departments_event)
            print("최종 이용 가능한 의사:", final_available_practitioners)
            # 직렬화
            practitionerserializer = PractitionerAppointmentSerializer(
                appointment_available_practitioners, many=True
            )

            return Response(practitionerserializer.data, status=status.HTTP_200_OK)
        # 부서만 선택 부서의 의사목록
        elif department and not (date or time or practitioner):
            # 해당 부서의 의사 목록 조회
            practitioners = Practitioner.objects.filter(department=department)
            practitioners_serializer = PractitionerAppointmentSerializer(
                practitioners, many=True)

            today = timezone.now().date()
            thirty_days_later = today + timedelta(days=30)
            available_times = {}
            holidays = self.get_hospital_holidays()
            # 각 의사의 예약 가능한 시간대 조회
            for practitioner in practitioners:
                booked_appointments = Appointment.objects.filter(
                    practitioner=practitioner,
                    start__date__range=[today, thirty_days_later]
                ).values_list('start', flat=True)

                # 의사의 연차 기간 조회
                annual_leaves = Annual.objects.filter(
                    practitioner=practitioner,
                    start_date__lte=thirty_days_later, end_date__gte=today
                ).values_list('start_date', 'end_date')

                # 예약된 시간대를 로컬 시간대로 변환하여 리스트로 저장
                booked_times = set(timezone.localtime(appointment).strftime(
                    '%Y-%m-%d %H:%M:%S') for appointment in booked_appointments)
                available_times[practitioner.id] = []

                # 연차 기간을 리스트로 저장
                annual_leave_days = set()
                for start_date, end_date in annual_leaves:
                    current_date = start_date
                    while current_date <= end_date:
                        annual_leave_days.add(current_date)
                        current_date += datetime.timedelta(days=1)

                for day in range(30):
                    date = today + timedelta(days=day)
                    if date in annual_leave_days or date in holidays:
                        continue  # 연차 기간이나 병원의 휴일이면 예약 가능한 시간대에서 제외

                    for hour in range(9, 18):  # 병원 운영시간
                        for minute in [0, 20, 40]:  # 예약단위는 20분
                            time_slot = datetime.combine(
                                date, dt_time(hour, minute))
                            local_time_slot = timezone.localtime(
                                timezone.make_aware(time_slot))
                            local_time_slot_str = local_time_slot.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            if local_time_slot_str not in booked_times:
                                available_times[practitioner.id].append(
                                    local_time_slot_str)
            # "available_times": available_times, "holidays": list(holidays)
            return Response(
                practitioners_serializer.data, status=status.HTTP_200_OK)

        # 의사만선택  해당 의사의 전체 스케줄(예약된 시간 포함)
        elif practitioner and not (date or time or department):
            today = timezone.now().date()
            thirty_days_later = today + timedelta(days=30)
            practitioner = Practitioner.objects.get(id=practitioner)
            holidays = self.get_hospital_holidays
            # 30일 기간 내의 모든 예약 조회
            appointments = Appointment.objects.filter(
                practitioner=practitioner,
                start__date__range=[today, thirty_days_later]
            ).order_by('start')
            # 30일 기간 내의 모든 연차 조회
            annual_leaves = Annual.objects.filter(
                practitioner=practitioner,
                start_date__lte=thirty_days_later,
                end_date__gte=today
            ).order_by('start_date')
            # 직렬화
            practitioner_data = PractitionerAppointmentSerializer(
                practitioner).data
            appointments_data = AppointmentScheduleSerializer(
                appointments, many=True).data
            practitioner_annual = AnnualSerializer(
                annual_leaves, many=True).data
            # 결과 구성
            result = [practitioner_data, appointments_data, practitioner_annual
                      ]

            return Response(result, status=status.HTTP_200_OK)
        # 일,시 선택 예약 가능한 의사 목록과 예약 가능한 상태
        elif date and time and not (department or practitioner):
            datetimes = datetime.combine(date, time)
            # 해당날자의 예약 조회
            appointments = Appointment.objects.filter(
                start=datetimes, active=True).values_list('practitioner_id', flat=True)
            # 부서 이벤트
            departments_event = DepartmentEvent.objects.filter(
                start_time__date__lte=date, end_time__date__gte=date) .values_list('department_id', flat=True)
            # 해당 날자의 연차인 의사 조회
            annual_practitioners = Annual.objects.filter(
                start_date__lte=datetimes, end_date__gte=datetimes).values_list('practitioner_id', flat=True)
            # 예약 있는 의사를 제외
            practitioners = Practitioner.objects.exclude(
                id__in=appointments).exclude(id__in=annual_practitioners).exclude(department__in=departments_event)
            # 직렬화
            practitioners_serializer = PractitionerAppointmentSerializer(
                practitioners, many=True).data

            return Response(practitioners_serializer, status=status.HTTP_200_OK)
        # 일 , 부서 선택 해당 날짜에 부서별로 예약 가능한 의사 목록과 시간대
        elif date and department and not (time or practitioner):
            # 해당 부서의 의사 조회
            department_practitioners = Practitioner.objects.filter(
                department_id=department)
            # 의사중 해당일의 연차중인 의사 조회
            annual_practitioners = Annual.objects.filter(
                start_date__lte=date, end_date__gte=date).values_list('practitioner_id', flat=True)
            # 부서 이벤트
            departments_event = DepartmentEvent.objects.filter(
                start_time__date__lte=date, end_time__date__gte=date) .values_list('department_id', flat=True)
            # 해당일의 연차중이거나 부서 이벤트 있는 의사 제외
            department_practitioners_anuual = department_practitioners.exclude(
                id__in=annual_practitioners).exclude(department__in=departments_event)

            # 예약 가능한 의사가 없는 경우 메시지 반환
            if not department_practitioners_anuual.exists():
                return Response({"message": "예약 가능한 의사가 없습니다."}, status=status.HTTP_200_OK)
            department_serializer = PractitionerAppointmentSerializer(
                department_practitioners_anuual, many=True).data
            # 각 의사별로 예약 가능한 시간대 계산
            available_times = []
            start_time = dt_time(9, 0)
            end_time = dt_time(18, 0)

            for practitioner in department_practitioners_anuual:
                practitioner_appointments = Appointment.objects.filter(
                    practitioner=practitioner,
                    start__date=date
                ).order_by('start')

                # 09:00부터 18:00까지 20분 단위로 시간대 생성
                current_time = datetime.combine(date, start_time)
                end_time_dt = datetime.combine(date, end_time)
                time_slots = []

                while current_time < end_time_dt:
                    slot_start = current_time.time()
                    slot_end = (current_time + timedelta(minutes=20)).time()

                    # 해당 시간대에 예약이 있는지 확인
                    if not practitioner_appointments.filter(start__time__lt=slot_end, end__time__gt=slot_start).exists():
                        time_slots.append(f"{slot_start.strftime('%H:%M')}")

                    current_time += timedelta(minutes=20)

                available_times.append({
                    'practitioner': PractitionerAppointmentSerializer(practitioner).data,
                    'available_times': time_slots
                })

            return Response(department_serializer, status=status.HTTP_200_OK)
        # 일, 의사 선택 해당 의사의 특정 날짜 스케줄(예약된 시간 포함) #
        elif date and practitioner and not (time or department):

            # 해당 의사 조회
            practitioners = Practitioner.objects.get(id=practitioner)
            # 부서 이벤트
            departments_event = DepartmentEvent.objects.filter(
                Q(start_time__date__lte=date, end_time__date__gte=date) & Q(department=practitioners.department)).values_list('department_id', flat=True)
            # 해당 의사가 연차인지 확인
            is_on_leave = Annual.objects.filter(
                practitioner_id=practitioner,
                start_date__lte=date,
                end_date__gte=date
            ).exists()
            if departments_event:
                return Response("부서이벤트 있슴", status=status.HTTP_200_OK)
            if is_on_leave:
                return Response({"message": "해당 의사는 선택한 날짜에 연차입니다."}, status=status.HTTP_200_OK)
            # 해당 날짜에 departmentevent가 있는지

            # 해당 의사의 특정 날짜 예약 조회
            appointments = Appointment.objects.filter(
                practitioner=practitioner,
                start__date=date
            ).order_by('start')

            # 09:00부터 18:00까지 20분 단위로 시간대 생성 및 예약된 시간 확인
            start_time = dt_time(9, 0)
            end_time = dt_time(18, 0)
            current_time = datetime.combine(date, start_time)
            end_time_dt = datetime.combine(date, end_time)
            time_slots = []

            while current_time < end_time_dt:
                slot_start = current_time.time()
                slot_end = (current_time + timedelta(minutes=20)).time()

                # 해당 시간대에 예약이 있는지 확인
                if not appointments.filter(start__time__lt=slot_end, end__time__gt=slot_start).exists():
                    time_slots.append(f"{slot_start.strftime('%H:%M')}")

                current_time += timedelta(minutes=20)

            practitioner_serializer = PractitionerAppointmentSerializer(
                practitioners)
            # 의사 정보와 예약 가능한 시간대 반환
            return Response(
                practitioner_serializer.data, status=status.HTTP_200_OK)
            # 'available_times': time_slots,
            # 'appointments': list(appointments.values('start', 'end'))

        # 시간 ,부서 선택 해당 시간대에 해당 부서의 예약 가능한 의사 목록
        elif time and department and not (date or practitioner):
            today = datetime.today().date()
            thirty_days_later = today + timedelta(days=30)
            # 해당 부서의 의사조회
            departments = Practitioner.objects.filter(department=department)
            # 각 의사별 오늘부터 30일까지의 연차조회
            anuuals = Annual.objects.filter(
                start_date__lte=today, end_date__gte=thirty_days_later)
            # 해당의사의 예약
            appointments = Appointment.objects.filter(
                start__date__lte=thirty_days_later, start__date__gte=today,
                start__time=time).values_list('practitioner_id', flat=True)
            # 부서이벤트
            practitioners = departments.exclude(
                id__in=anuuals).exclude(id__in=appointments)

            final_practitioner = PractitionerAppointmentSerializer(
                practitioners, many=True)

            return Response(final_practitioner.data, status=status.HTTP_200_OK)

        # 시간 ,의사 선택 해당 시간에 의사의 예약 상태(예약 가능 여부)
        elif time and practitioner and not (date or department):
            try:
                practitioners = Practitioner.objects.get(
                    id=practitioner)
            except Exception as e:
                return Response(f"{e}해당의사가 없슴두", status=status.HTTP_400_BAD_REQUEST)
            today = datetime.today().date()
            thirty_days_later = today + timedelta(days=30)
            holidays = self.get_hospital_holidays()
            # 해당 의사 오늘부터 30일까지의 연차조회
            annuals = Annual.objects.filter(
                practitioner_id=practitioner,
                start_date__lte=thirty_days_later, end_date__gte=today)
            annuals_data = AnnualSerializer(annuals, many=True).data
            # 연차 날짜들을 집합으로 저장
            annual_leave_days = set()
            for annual in annuals:
                current_date = annual.start_date
                while current_date <= annual.end_date:
                    annual_leave_days.add(current_date)
                    current_date += timedelta(days=1)
            # 30일 내로 해당 시간에 예약이 가능한 목록 조회
            available_times = []
            start_time = dt_time(9, 0)
            end_time = dt_time(18, 0)

            for single_date in (today + timedelta(n) for n in range(31)):
                if single_date in holidays or single_date in annual_leave_days:
                    continue
                practitioner_appointments = Appointment.objects.filter(
                    practitioner=practitioner,
                    start__date=single_date,
                    start__time=time
                ).exists()

                # 해당 시간대에 예약이 있는지 확인
                if not practitioner_appointments:
                    available_times.append(single_date.strftime('%Y-%m-%d'))

            return Response(
                PractitionerAppointmentSerializer(practitioners).data,
                # '예약 가능한 일': available_times,
                # '의사님 쉬는날 ': annuals_data,
                # '병원 휴일': holidays
                status=status.HTTP_200_OK)

        # 부서 ,의사 선택 해당 부서에서 특정 의사의 스케줄 의사만 선택과 같네
        elif department and practitioner and not (date or time):
            today = timezone.now().date()
            thirty_days_later = today + timedelta(days=30)
            try:
                practitioner = Practitioner.objects.get(
                    id=practitioner, department=department)
            except Exception as e:
                return Response(f"{e}의사 또는 부서를 확인해 주세요", status=status.HTTP_400_BAD_REQUEST)
            holidays = self.get_hospital_holidays
            # 30일 기간 내의 모든 예약 조회
            appointments = Appointment.objects.filter(
                practitioner=practitioner,
                start__date__range=[today, thirty_days_later]
            ).order_by('start')
            # 30일 기간 내의 모든 연차 조회
            annual_leaves = Annual.objects.filter(
                practitioner=practitioner,
                start_date__lte=thirty_days_later,
                end_date__gte=today
            ).order_by('start_date')
            # 직렬화
            practitioner_data = PractitionerAppointmentSerializer(
                practitioner).data
            appointments_data = AppointmentScheduleSerializer(
                appointments, many=True).data
            practitioner_annual = AnnualSerializer(
                annual_leaves, many=True).data
            # 결과 구성
            result = {
                practitioner_data,
                appointments_data,
                practitioner_annual
            }

            return Response(result, status=status.HTTP_200_OK)
        elif date and time and department and not practitioner:  # 일,시,부서선택 특정 날짜와 시간대에 해당 부서의 예약 가능한 의사 목록과 상태
            datetimes = datetime.combine(date, time)
            # 해당부서 의사 조회
            departments = Practitioner.objects.filter(department=department)
            # 의사들의  연차 여부 확인
            annuals = Annual.objects.filter(
                start_date__lte=date, end_date__gte=date).values_list('practitioner_id', flat=True)
            # 연차인 의사 제외
            practitioners = departments.exclude(id__in=annuals)
            # 의사들의 예약 조회
            appointments = Appointment.objects.filter(start=datetimes)
            # 예약있는 의사 제외
            practitioners_appointments = practitioners.exclude(
                id__in=appointments)
            # 부서이벤트 있는지 조회
            department_event = DepartmentEvent.objects.filter(
                start_time__date__lte=date, end_time__date__gte=date).values_list('department_id', flat=True)
            # 부서이벤트에 포함된 의사 제외
            department_practitioners = practitioners_appointments.exclude(
                department__in=department_event)
            final_practitoner = PractitionerAppointmentSerializer(
                department_practitioners, many=True)

            return Response(final_practitoner.data, status=status.HTTP_200_OK)
        # 일,시 ,의사 선택 특정 날짜와 시간대에 의사의 예약 상태(예약 가능 여부)
        elif date and time and practitioner and not department:
            datetimes = datetime.combine(date, time)
            # 해당 의사 조회
            practitioners = Practitioner.objects.get(id=practitioner)
            # 해당의사가 해당일에 연차인지
            annuals = Annual.objects.filter(
                practitioner_id=practitioner, start_date__lte=date, end_date__gte=date)
            if annuals:
                return Response(f"해당의사는 {date}일 연차입니다 ")
            # 해당의사의 datetime의 예약이 있는지
            appointments = Appointment.objects.filter(
                practitioner_id=practitioner, start=datetimes)
            if appointments:
                return Response(f"{practitioner}의사는 {datetimes}에 예약이 있습니다.")
            # 부서 이벤트
            department_event = DepartmentEvent.objects.filter(
                start_time__date__lte=date, end_time__date__gte=date, department=practitioners.department).values_list('department_id', flat=True)
            if department_event:
                return Response("부서이벤트로 인한 예약 불가")
            final_practitioner = PractitionerAppointmentSerializer(
                practitioners).data
            return Response(final_practitioner, status=status.HTTP_200_OK)
        elif date and department and practitioner and not time:  # 일,부서,의사 선택 특정 날짜에 해당 부서와 의사의 예약 상태 의사와 일선택과 같음
            # 해당 의사 조회
            try:
                practitioners = Practitioner.objects.get(
                    id=practitioner, department=department)
            except Exception as e:
                return Response(f"{e}의사 또는 부서를 확인해 주세요", status=status.HTTP_400_BAD_REQUEST)
            # 해당 의사가 연차인지 확인
            is_on_leave = Annual.objects.filter(
                practitioner_id=practitioner,
                start_date__lte=date,
                end_date__gte=date
            ).exists()

            if is_on_leave:
                return Response({"message": "해당 의사는 선택한 날짜에 연차입니다."}, status=status.HTTP_200_OK)
            # 부서 이벤트
            departments_event = DepartmentEvent.objects.filter(
                start_time__date__lte=date, end_time__date__gte=date, department=practitioners.department).exists()
            if departments_event:
                return Response("부서이벤트로인한 예약 불가")
            # 해당 의사의 특정 날짜 예약 조회
            appointments = Appointment.objects.filter(
                practitioner=practitioner,
                start__date=date
            ).order_by('start')

            # 09:00부터 18:00까지 20분 단위로 시간대 생성 및 예약된 시간 확인
            start_time = dt_time(9, 0)
            end_time = dt_time(18, 0)
            current_time = datetime.combine(date, start_time)
            end_time_dt = datetime.combine(date, end_time)
            time_slots = []

            while current_time < end_time_dt:
                slot_start = current_time.time()
                slot_end = (current_time + timedelta(minutes=20)).time()

                # 해당 시간대에 예약이 있는지 확인
                if not appointments.filter(start__time__lt=slot_end, end__time__gt=slot_start).exists():
                    time_slots.append(f"{slot_start.strftime('%H:%M')}")

                current_time += timedelta(minutes=20)

            practitioner_serializer = PractitionerAppointmentSerializer(
                practitioners)
            # 의사 정보와 예약 가능한 시간대 반환
            return Response(
                practitioner_serializer.data,
                # 'available_times': time_slots,
                # 'appointments': list(appointments.values('start', 'end'))
                status=status.HTTP_200_OK)
        # 시 ,부서,의사 선택 특정 시간대에 해당 부서와 의사의 예약 상태 의사,시 선택과 같음
        elif time and department and practitioner and not date:
            try:
                practitioners = Practitioner.objects.get(
                    id=practitioner, department=department)
            except Exception as e:
                return Response(f"{e}의사 또는 부서를 확인해 주세요", status=status.HTTP_400_BAD_REQUEST)
            today = datetime.today().date()
            thirty_days_later = today + timedelta(days=30)
            holidays = self.get_hospital_holidays()
            # 해당 의사 오늘부터 30일까지의 연차조회
            annuals = Annual.objects.filter(
                practitioner_id=practitioner,
                start_date__lte=thirty_days_later, end_date__gte=today)
            annuals_data = AnnualSerializer(annuals, many=True).data
            print(annuals_data, today, thirty_days_later,
                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # 연차 날짜들을 집합으로 저장
            annual_leave_days = set()
            for annual in annuals:
                current_date = annual.start_date
                while current_date <= annual.end_date:
                    annual_leave_days.add(current_date)
                    current_date += timedelta(days=1)
            # 30일 내로 해당 시간에 예약이 가능한 목록 조회
            available_times = []
            start_time = dt_time(9, 0)
            end_time = dt_time(18, 0)

            for single_date in (today + timedelta(n) for n in range(31)):
                if single_date in holidays or single_date in annual_leave_days:
                    continue
                practitioner_appointments = Appointment.objects.filter(
                    practitioner=practitioner,
                    start__date=single_date,
                    start__time=time
                ).exists()

                # 해당 시간대에 예약이 있는지 확인
                if not practitioner_appointments:
                    available_times.append(single_date.strftime('%Y-%m-%d'))

            return Response(
                PractitionerAppointmentSerializer(practitioners).data,
                # '예약 가능한 일': available_times,
                # '의사님 쉬는날 ': annuals_data,
                # '병원 휴일': holidays
                status=status.HTTP_200_OK)

        # 일,시,부서,의사 선택 특정 날짜와 시간대에 해당 부서와 의사의 예약 상태(예약 가능 여부) 일,시,의사와 같음
        elif date and time and department and practitioner:
            datetimes = datetime.combine(date, time)
            # 해당 의사 조회
            try:
                practitioners = Practitioner.objects.get(
                    id=practitioner, department=department)
            except Exception as e:
                return Response(f"{e}의사 또는 부서를 확인해 주세요", status=status.HTTP_400_BAD_REQUEST)
            # 해당의사가 해당일에 연차인지
            annuals = Annual.objects.filter(
                practitioner_id=practitioner, start_date__lte=date, end_date__gte=date)
            if annuals:
                return Response(f"해당의사는 {date}일 연차입니다 ")
            # 부서 이벤트
            department_event = DepartmentEvent.objects.filter(
                start_time__date__lte=date, end_time__date__gte=date, department=practitioners.department).values_list('department_id', flat=True)
            if department_event:
                return Response("부서이벤트로 인한 예약 불가")
            # 해당의사의 datetime의 예약이 있는지
            appointments = Appointment.objects.filter(
                practitioner_id=practitioner, start=datetimes)
            if appointments:
                return Response(f"{practitioner}의사는 {datetimes}에 예약이 있습니다.")
            final_practitioner = PractitionerAppointmentSerializer(
                practitioners).data
            return Response(final_practitioner, status=status.HTTP_200_OK)

        return Response("잘못된 선택입니다", status=status.HTTP_400_BAD_REQUEST)



class WaitingListView(APIView):
    paginator = PageNumberPagination()

    def get(self, request):
        now = timezone.now()
        start_time = now + timedelta(hours=12)
        end_time = now - timedelta(hours=1)

        appointments = Appointment.objects.filter(start__lte=start_time, end__gte=end_time).exclude(
            status__in=['cancelled', 'noshow', 'fulfilled']).order_by('start')

        page = self.paginator.paginate_queryset(
            appointments, request, view=self)

        serializer = AppointmentSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)



class AiConsultationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({"error": "증상을 설명해주세요"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ai_response = chatgpt(user_message)
            return Response({"response": ai_response}, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "에러가 발생했습니다:  " + str(e)
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
