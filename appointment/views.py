from .models import Appointment, Practitioner, Department
from datetime import datetime as dt, timedelta, time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSreailizer, AppointmentListSerializer, PractitionerAppointmentSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import Patient, Account, ContactPoint
from .models import Appointment
from django.contrib.auth.hashers import check_password


class AppointMentAPIView(APIView):  # 예약기능 CRUD
    permission_classes = [IsAuthenticated]

    def get_patient(self, patient_id):
        return get_object_or_404(Patient, pk=patient_id)

    def post(self, request, patient_id):
        patient = self.get_patient(patient_id)

        serializer = AppointmentSreailizer(
            data=request.data, context={'patient': patient})
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
        datetime = request.data.get('datetime')
        password = request.data.get('password')
        appointments = Appointment.objects.filter(
            patient=patient, datetime=datetime)
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
            # date = serializer.validated_data.get('date')
            # time = serializer.validated_data.get('time')
            datetime = serializer.validated_data.get('datetime')
            # if not time:
            #     return Response("시간을 선택하세요")
            # datetime = dt.combine(date, time)
            query = Appointment.objects.filter(active=True)
            if department:
                query = query.filter(department=department)
            if practitioner:
                query = query.filter(practitioner=practitioner)
            if datetime:
                query = query.filter(datetime=datetime)
            if not datetime and not practitioner:
                # 의사 전체 반환
                departments = Department.objects.get(id=department.id)
                departments_practitioner = Department.objects.filter(
                    department=departments.department)
                val_department = PractitionerAppointmentSerializer(
                    departments_practitioner, many=True)
                return Response({
                    "message": "해당과의 의사",
                    "data": val_department.data
                }, status=status.HTTP_200_OK)

            if not practitioner and datetime:  # 시간만 조회
                # 예약된 시간대에 대한 쿼리 준비
                booked_appointments = Appointment.objects.filter(
                    datetime=datetime, active=True)
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
