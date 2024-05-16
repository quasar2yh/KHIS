from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSreailizer
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import Patient
from .models import Appointment


class AppointMentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
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
        patient = get_object_or_404(Patient, pk=patient_id)
        appointments = Appointment.objects.filter(patient=patient)
        serializer = AppointmentSreailizer(appointments, many=True)
        return Response(serializer.data)
