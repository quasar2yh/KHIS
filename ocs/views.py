from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import Patient
from account.serializers import PatientSerializer


class PatientAPIView(APIView):
    # 환자 데이터 추가
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 환자 데이터 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        serializer = PatientSerializer(patient)
        return Response(data=serializer.data)
