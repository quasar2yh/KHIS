from .tasks import send_email_async
from django.core.mail import send_mail
from .serializers import MailSerializer
import requests
import datetime
from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Annual, HospitalSchedule, DepartmentEvent
from .serializers import AnnualSerializer, HospitalScheduleSerializer, DepartmentEventSerializer
from django.utils.dateparse import parse_date
from .utils import save_holidays_from_api
from account.models import Department, Practitioner
from account.serializers import DepartmentSerializer, PractitionerSerializer
from rest_framework.permissions import AllowAny


# 연차신청

class MedicalScheduleAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            serializer = AnnualSerializer(data=request.data)
            if serializer.is_valid():
                practitioner = request.user.practitioner
                start_date = serializer.validated_data['start_date']
                end_date = serializer.validated_data['end_date']

                # 중복 검사
                overlapping_annuals = Annual.objects.filter(
                    practitioner=practitioner,
                    start_date__lte=end_date,
                    end_date__gte=start_date
                )
                if overlapping_annuals.exists():
                    return Response({"message": "이미 신청된 날짜입니다."}, status=status.HTTP_400_BAD_REQUEST)

                reason = serializer.validated_data.get('reason', '')
                annual = Annual.objects.create(
                    practitioner=practitioner, start_date=start_date, end_date=end_date, reason=reason)
                return Response({"message": "연차 신청이 완료되었습니다."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 본인 연차 조회 (시작 일 빠른 순)


    def get(self, request):
        if request.user.is_authenticated:
            practitioner = request.user.practitioner
            annuals = Annual.objects.filter(
                practitioner=practitioner).order_by('-start_date')
            serializer = AnnualSerializer(annuals, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 본인 연차 구간조회 (시작 일 빠른 순)

class SpecificScheduleAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            practitioner = request.user.practitioner

            # 시작 날짜와 끝 날짜 가져오기
            start_date_str = request.data.get('start_date')
            end_date_str = request.data.get('end_date')

            if not start_date_str or not end_date_str:
                return Response({"message": "시작 날짜와 끝 날짜를 지정해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                start_date = datetime.strptime(
                    start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"message": "올바른 날짜 형식이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

            # 연차 조회
            annuals = Annual.objects.filter(
                practitioner=practitioner,
                start_date__lte=end_date,
                end_date__gte=start_date
            ).order_by('-start_date')
            serializer = AnnualSerializer(annuals, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 전체 직원 연차 조회 (시작 일 빠른 순)

class MedicalIntegratedAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_practitioner():
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_403_FORBIDDEN)

        medical_staff_schedules = Annual.objects.all().order_by('-start_date')
        medical_staff_serializer = AnnualSerializer(
            medical_staff_schedules, many=True)
        return Response(medical_staff_serializer.data, status=status.HTTP_200_OK)


# 전체 직원 연차의 구간 조회 (시작 일 빠른 순)

class MedicalSpecificIntegratedAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():

            # 시작 날짜와 끝 날짜 가져오기
            start_date_str = request.data.get('start_date')
            end_date_str = request.data.get('end_date')

            if not start_date_str or not end_date_str:
                return Response({"message": "시작 날짜와 끝 날짜를 지정해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                start_date = datetime.strptime(
                    start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"message": "올바른 날짜 형식이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

            annuals = Annual.objects.filter(
                start_date__lte=end_date,
                end_date__gte=start_date
            ).order_by('-start_date')

            serializer = AnnualSerializer(annuals, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)

 # 병원 자체 휴일 등록 및 조회


class HospitalScheduleAPIView(APIView):
    def post(self, request):
        date = request.data.get('date')
        if HospitalSchedule.objects.filter(date=date, is_hospital_holiday=True).exists():
            return Response({"error": "이미 등록된 휴일입니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HospitalScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_hospital_holiday=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        hospital_holidays = HospitalSchedule.objects.filter(
            is_hospital_holiday=True)
        serializer = HospitalScheduleSerializer(hospital_holidays, many=True)
        return Response(serializer.data)


# 병원 자체 휴일 수정 및 삭제


class HospitalScheduleDetailAPIView(APIView):
    def put(self, request, hospitalschedule_id):
        try:
            schedule = HospitalSchedule.objects.get(id=hospitalschedule_id)
            serializer = HospitalScheduleSerializer(
                schedule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except HospitalSchedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, hospitalschedule_id):
        try:
            schedule = HospitalSchedule.objects.get(id=hospitalschedule_id)
            schedule.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HospitalSchedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# 공공 데이터 API로 공휴일 데이터 조회

class HospitalPublicScheduleAPIView(APIView):
    def get(self, request):
        # 공휴일 DB 저장
        save_holidays_from_api()

        # 모든 공휴일 조회
        public_holidays = HospitalSchedule.objects.filter(
            is_public_holiday=True)

        serializer = HospitalScheduleSerializer(public_holidays, many=True)
        return Response(serializer.data)


# 전체 의료진 스케줄 + 전체 병원 스케줄 조회 (필요한지 기능인지 검토 필요)

class IntegratedScheduleAPIView(APIView):
    def get(self, request):
        hospital_schedules = HospitalSchedule.objects.all()
        hospital_serializer = HospitalScheduleSerializer(
            hospital_schedules, many=True)

        # 의료진 전체 스케줄 조회
        medical_staff_schedules = Annual.objects.all()
        medical_staff_serializer = AnnualSerializer(
            medical_staff_schedules, many=True)

        # 병원 휴일과 의료진 전체 스케줄을 통합하여 응답
        integrated_data = {
            "hospital_schedules": hospital_serializer.data,
            "medical_staff_schedules": medical_staff_serializer.data
        }
        return Response(integrated_data)

 # 부서등록


class DepartmentRegisterAPIView(APIView):
    def post(self, request):
        department_name = request.data.get('department_name')

        # 부서 이름 중복 확인
        if Department.objects.filter(department_name=department_name).exists():
            return Response({'error': '부서 이름이 이미 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 데이터를 데이터베이스에 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 # 부서목록 조회


class DepartmentListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

 # 부서별 연차 조회


class DepartmentMedicalScheduleAPIView(APIView):
    def get(self, request, department_id):
        practitioners = Practitioner.objects.filter(
            department_id=department_id)
        annuals = Annual.objects.filter(
            practitioner__in=practitioners).order_by('start_date')
        serializer = AnnualSerializer(annuals, many=True)
        return Response(serializer.data)


# 부서별 의료진 조회

class DepartmentPractitionerAPIView(APIView):
    permission_classes = [AllowAny]

    def get(seif, request, department_id):
        practitioners = Practitioner.objects.filter(
            department_id=department_id)
        serializer = PractitionerSerializer(practitioners, many=True)
        return Response(serializer.data)

 # 부셔별 일정 등록


class DepartmentEventAPIView(APIView):
    def post(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response({"error": "Department does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, department_id):
        department_events = DepartmentEvent.objects.filter(
            department_id=department_id)
        serializer = DepartmentEventSerializer(department_events, many=True)
        return Response(serializer.data)


# 부셔별 일정 수정 및 삭제

class DepartmentEventDetailAPIView(APIView):
    def put(self, request, department_id, event_id):
        try:
            department_event = DepartmentEvent.objects.get(
                id=event_id, department_id=department_id)
        except DepartmentEvent.DoesNotExist:
            return Response({"error": "Department event does not exist"}, status=status.HTTP_404_NOT_FOUND)

        request_data = request.data.copy()
        request_data.pop('id', None)
        request_data.pop('department', None)

        serializer = DepartmentEventSerializer(
            department_event, data=request.data,  partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, department_id, event_id):
        try:
            department_event = DepartmentEvent.objects.get(
                id=event_id, department_id=department_id)
        except DepartmentEvent.DoesNotExist:
            return Response({"error": "Department event does not exist"}, status=status.HTTP_404_NOT_FOUND)

        department_event.delete()
        return Response({"success": "일정이 성공적으로 삭제되었습니다"}, status=status.HTTP_204_NO_CONTENT)


# 의료진 알람 메일 발송

class MailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            # Celery를 사용하여 작업을 예약합니다.
            send_email_async.delay(
                subject, message, 'ritsukoice@naver.com', email)
            return Response({"success": "메일이 예약되었습니다"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
