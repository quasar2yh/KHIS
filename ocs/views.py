from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Patient
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer


class MedicalRecordAPIView(APIView):
    # 환자 진료 기록 생성
    def post(self, request, patient_id):
        request.data['patient'] = patient_id
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)
    
    # 환자 진료 기록 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        medical_records = patient.medicalrecord_set.all()
        if not medical_records:
            return Response(message="진료 기록이 없습니다.")
        serializer = MedicalRecordSerializer(medical_records, many=True)
        return Response(data=serializer.data)
    
    # 환자 진료 기록 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        medical_records = patient.medicalrecord_set.all()
        if not medical_records:
            return Response(message="진료 기록이 없습니다.")
        serializer = MedicalRecordSerializer(medical_records, many=True)
        return Response(data=serializer.data)