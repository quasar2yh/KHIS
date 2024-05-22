
from django.utils import timezone
from .open_ai import chatgpt
from .models import Appointment, Practitioner, Department
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import AppointmentSreailizer, AppointmentListSerializer, PractitionerAppointmentSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import Patient
from .models import Appointment
from django.contrib.auth.hashers import check_password


class AppointMentAPIView(APIView):  # 예약기능 CRUD
    permission_classes = [IsAuthenticated]

    def get_patient(self, patient_id):
        return get_object_or_404(Patient, pk=patient_id)

    def post(self, request, patient_id):
        patient = self.get_patient(patient_id)
        subject = request.user.subject
        serializer = AppointmentSreailizer(
            data=request.data, context={'patient': patient, 'subject': subject})
        if serializer.is_valid(raise_exception=True):
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, patient_id):
        patient = self.get_patient(patient_id)
        appointments = Appointment.objects.filter(patient=patient)
        serializer = AppointmentSreailizer(appointments, many=True)
        return Response(serializer.data)

    def delete(self, request, patient_id):
        patient = self.get_patient(patient_id)
        account = patient.account
        start = request.data.get('start')
        password = request.data.get('password')
        appointments = Appointment.objects.filter(
            patient=patient, start=start)
        if check_password(password, account.password):
            appointments.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("응~비번 틀림~", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, patient_id):
        patient = self.get_patient(patient_id)
        appointment = get_object_or_404(Appointment, patient=patient)
        account = patient.account
        login_id = request.user.id
        if account.id == login_id:
            serializer = AppointmentSreailizer(
                appointment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


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
            if not start and not practitioner:
                # 의사 전체 반환 어떻게 하징
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
                print(start)
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

        serializer = AppointmentSreailizer(page, many=True)
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
