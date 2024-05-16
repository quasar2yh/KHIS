from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSreailizer
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import Patient


class AppointMentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        serializer = AppointmentSreailizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
