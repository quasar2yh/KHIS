from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSreailizer
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import Patient, Account
from .models import Appointment
from django.contrib.auth.hashers import check_password


class AppointMentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_patient(self, patient_id):
        return get_object_or_404(Patient, pk=patient_id)

    def post(self, request, patient_id):
        patient = self.get_patient(patient_id)
        active_appointments = Appointment.objects.filter(
            patient=patient, active=True)

        if active_appointments.exists():
            return Response({"detail": "이미 진행 중인 예약이 있어 새로운 예약을 할 수 없습니다."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = AppointmentSreailizer(data=request.data)
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
        password = request.data.get('password')
        appointments = Appointment.objects.filter(patient=patient)
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
