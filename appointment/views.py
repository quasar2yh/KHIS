
from django.utils import timezone
from .open_ai import chatgpt
from .models import Appointment, Practitioner, Department
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import AppointmentSerializer, AppointmentListSerializer, PractitionerAppointmentSerializer, AppointmentDelSerializer, HospitalScheduleSerializer, AnnualSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import Patient
from django.contrib.auth.hashers import check_password
from django.utils.dateparse import parse_datetime, parse_time, parse_date
from schedule.models import Annual, HospitalSchedule
import datetime


class AppointMentAPIView(APIView):  # 예약기능 CRUD
    permission_classes = [IsAuthenticated]

    def get_patient(self, patient_id):

        return get_object_or_404(Patient, pk=patient_id)

    def post(self, request, patient_id):
        patient = self.get_patient(patient_id)
        subject = request.user.subject
        serializer = AppointmentSerializer(
            data=request.data, context={'patient': patient, 'subject': subject})
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            appointment = Appointment(**validated_data)
            appointment.patient = patient
            appointment.appointment_clean_and_save = True
            appointment.save()
            appointment.appointment_clean_and_save = False
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, patient_id):
        patient = self.get_patient(patient_id)
        practitioner = request.query_params.get('practitioner')
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        appointments = Appointment.objects.filter(
            patient=patient).order_by('-created')
        if not patient:
            return Response("환자 정보가 없습니다.")
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
        appointment = get_object_or_404(Appointment, patient=patient)
        account = patient.account
        login_id = request.user.id
        if account.id == login_id:
            serializer = AppointmentSerializer(
                appointment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AppointMentDateAPIView(APIView):  # 시간으로 조회
    def get(self, request):
        practitioner = request.query_params.get('practitioner')
        date = request.query_params.get('date')

        return Response("가리겟겟")


class AppointmentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

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

    def get(self, request):
        department = request.query_params.get('department')
        date = request.query_params.get('date')
        time = request.query_params.get('time')
        practitioner = request.query_params.get('practitioner')
        if date:
            date = parse_date(date)
        if time:
            time = parse_time(time)

        # 일만 선택->해당 날짜에 예약 가능한 의사 목록
        if date and not (time or department or practitioner):
            practitioner = Annual.objects.filter(
                start_date__lte=date, end_date__gte=date)

            # 병원의 휴일인지 아닌지
            try:
                hospital = HospitalSchedule.objects.get(date=date)
                if hospital.is_hospital_holiday or hospital.is_public_holiday:
                    return Response({"message": "병원의 휴일입니다."}, status=status.HTTP_200_OK)
            except HospitalSchedule.DoesNotExist:
                pass

            # 쉬는 의사를 제외한 나머지 의사 조회
            available_practitioners = Practitioner.objects.exclude(
                id__in=practitioner)
            practitionerserializer = PractitionerAppointmentSerializer(
                available_practitioners, many=True)

            return Response(f"일 선택 완료: {date} 예약가능한 의사:{practitionerserializer.data}", status=status.HTTP_200_OK)
        elif time and not (date or department or practitioner):  # 시간만 선택 해당시간에 예약 가능한 의사
            today = datetime.date.today()
            thirty_days_later = today + datetime.timedelta(days=30)

            # 병원의 휴일 조회
            hospital_holidays = HospitalSchedule.objects.filter(
                date__range=[today, thirty_days_later],
                is_hospital_holiday=True
            ).values_list('date', flat=True) | HospitalSchedule.objects.filter(
                date__range=[today, thirty_days_later],
                is_public_holiday=True
            ).values_list('date', flat=True)

            holidays = list(hospital_holidays)

            # 30일 안으로 연차 있는 의사 조회
            resting_practitioners = Annual.objects.filter(
                start_date__lte=thirty_days_later, end_date__gte=today
            ).values_list('practitioner_id', flat=True)

            # 연차가 끝나는 날이 오늘 이후인 의사도 포함
            available_practitioners_ids = Practitioner.objects.exclude(
                id__in=resting_practitioners
            ).values_list('id', flat=True)

            # 해당 시간에 예약이 있는 의사 조회
            booked_practitioners = Appointment.objects.filter(
                start__date__range=[today, thirty_days_later],
                start__time=time
            ).values_list('practitioner_id', flat=True)

            # 예약이 있는 의사 중 해당 시간에 예약이 하나라도 비어있는 의사 포함
            available_practitioners_with_empty_slots = Practitioner.objects.exclude(
                id__in=booked_practitioners
            ).values_list('id', flat=True)

            final_available_practitioners_ids = Practitioner.objects.filter(
                id__in=available_practitioners_ids
            ).exclude(
                id__in=booked_practitioners
            ).values_list('id', flat=True) | Practitioner.objects.filter(
                id__in=available_practitioners_ids
            ).filter(
                id__in=available_practitioners_with_empty_slots
            ).values_list('id', flat=True)

            final_available_practitioners = Practitioner.objects.filter(
                id__in=final_available_practitioners_ids
            )

            practitionerserializer = PractitionerAppointmentSerializer(
                final_available_practitioners, many=True
            )

            return Response(f"시간 선택 완료: {time} 병원휴일{holidays} 예약가능한 의사: {practitionerserializer.data}", status=status.HTTP_200_OK)
        # 부서만 선택 부서의 의사목록과 의사별 예약 가능한 시간대
        elif department and not (date or time or practitioner):
            # 해당 부서의 의사 목록 조회
            practitioners = Practitioner.objects.filter(department=department)
            practitioners_serializer = PractitionerAppointmentSerializer(
                practitioners, many=True)

            # 각 의사의 예약 가능한 시간대 조회
            today = timezone.now().date()
            thirty_days_later = today + datetime.timedelta(days=30)
            available_times = {}

            # 병원의 휴일 조회
            hospital_holidays = HospitalSchedule.objects.filter(
                date__range=[today, thirty_days_later],
                is_hospital_holiday=True
            ).values_list('date', flat=True) | HospitalSchedule.objects.filter(
                date__range=[today, thirty_days_later],
                is_public_holiday=True
            ).values_list('date', flat=True)

            holidays = set(hospital_holidays)

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
                    date = today + datetime.timedelta(days=day)
                    if date in annual_leave_days or date in holidays:
                        continue  # 연차 기간이나 병원의 휴일이면 예약 가능한 시간대에서 제외

                    for hour in range(9, 18):  # 병원 운영시간
                        for minute in [0, 20, 40]:  # 예약단위는 20분
                            time_slot = datetime.datetime.combine(
                                date, datetime.time(hour, minute))
                            local_time_slot = timezone.localtime(
                                timezone.make_aware(time_slot))
                            local_time_slot_str = local_time_slot.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            if local_time_slot_str not in booked_times:
                                available_times[practitioner.id].append(
                                    local_time_slot_str)

            return Response({
                "message": "부서 선택 완료",
                "practitioners": practitioners_serializer.data,
                "available_times": available_times,
                "holidays": list(holidays)
            }, status=status.HTTP_200_OK)

        # 의사만선택  해당 의사의 전체 스케줄(예약된 시간 포함)
        elif practitioner and not (date or time or department):
            return Response(f"의사 선택 완료: {practitioner}", status=status.HTTP_200_OK)
        # 일,시 선택 예약 가능한 의사 목록과 예약 가능한 상태
        elif date and time and not (department or practitioner):
            return Response(f"예약 가능한 의사 선택 완료: 일-{date}, 시간-{time}", status=status.HTTP_200_OK)
        # 일 , 부서 선택 해당 날짜에 부서별로 예약 가능한 의사 목록과 시간대
        elif date and department and not (time or practitioner):
            return Response(f"일과 부서 선택 완료: 일-{date}, 부서-{department}", status=status.HTTP_200_OK)
        # 일, 의사 선택 해당 의사의 특정 날짜 스케줄(예약된 시간 포함)
        elif date and practitioner and not (time or department):
            return Response(f"일과 의사 선택 완료: 일-{date}, 의사-{practitioner}", status=status.HTTP_200_OK)
        # 시간 ,부서 선택 해당 시간대에 해당 부서의 예약 가능한 의사 목록
        elif time and department and not (date or practitioner):
            return Response(f"시간과 부서 선택 완료: 시간-{time}, 부서-{department}", status=status.HTTP_200_OK)
        # 시간 ,의사 선택 해당 시간에 의사의 예약 상태(예약 가능 여부)
        elif time and practitioner and not (date or department):
            return Response(f"시간과 의사 선택 완료: 시간-{time}, 의사-{practitioner}", status=status.HTTP_200_OK)
        # 부서 ,의사 선택 해당 부서에서 특정 의사의 스케줄 의사만 선택과 같네
        elif department and practitioner and not (date or time):
            return Response(f"부서와 의사 선택 완료: 부서-{department}, 의사-{practitioner}", status=status.HTTP_200_OK)
        elif date and time and department and not practitioner:  # 일,시,부서선택 특정 날짜와 시간대에 해당 부서의 예약 가능한 의사 목록과 상태
            return Response(f"일, 시간, 부서 선택 완료: 일-{date}, 시간-{time}, 부서-{department}", status=status.HTTP_200_OK)
        # 일,시 ,의사 선택 특정 날짜와 시간대에 의사의 예약 상태(예약 가능 여부)
        elif date and time and practitioner and not department:
            return Response(f"일, 시간, 의사 선택 완료: 일-{date}, 시간-{time}, 의사-{practitioner}", status=status.HTTP_200_OK)
        elif date and department and practitioner and not time:  # 일,부서,의사 선택 특정 날짜에 해당 부서와 의사의 예약 상태 의사와 일선택과 같음
            return Response(f"일, 부서, 의사 선택 완료: 일-{date}, 부서-{department}, 의사-{practitioner}", status=status.HTTP_200_OK)
        # 시 ,부서,의사 선택 특정 시간대에 해당 부서와 의사의 예약 상태 의사,시 선택과 같음
        elif time and department and practitioner and not date:
            return Response(f"시간, 부서, 의사 선택 완료: 시간-{time}, 부서-{department}, 의사-{practitioner}", status=status.HTTP_200_OK)
        # 일,시,부서,의사 선택 특정 날짜와 시간대에 해당 부서와 의사의 예약 상태(예약 가능 여부) 일,시,의사와 같음
        elif date and time and department and practitioner:
            return Response(f"일, 시간, 부서, 의사 선택 완료: 일-{date}, 시간-{time}, 부서-{department}, 의사-{practitioner}", status=status.HTTP_200_OK)
        else:
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
