from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import Patient
from account.serializers import PatientSerializer
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

    
class PatientAPIView(APIView):
    # 환자 데이터 생성
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

    # 환자 데이터 수정
    def put(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)


class MedicalRecordAPIView(APIView):
    # 환자 진료 기록 생성
    def post(self, request, patient_id):
        request.data['patient'] = patient_id
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 환자 진료 기록 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        medical_records = patient.medicalrecord_set.all()
        if not medical_records:
            return Response(message="진료 기록이 없습니다.")
        serializer = MedicalRecordSerializer(medical_records, many=True)
        return Response(data=serializer.data)