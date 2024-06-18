from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Patient
from .models import ProcedureRecord
from .serializers import MedicalRecordSerializer, ProcedureRecordSerializer


class MedicalRecordAPIView(APIView):
    # 환자 진료 기록 생성
    def post(self, request):
        if request.user.is_authenticated and request.user.is_practitioner:
            serializer = MedicalRecordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 환자 진료 기록 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        medical_records = patient.medicalrecord_set.all()
        if not medical_records:
            return Response({"detail": "진료 기록이 없습니다."})
        serializer = MedicalRecordSerializer(
            instance=medical_records, many=True)
        return Response(data=serializer.data)

    # 환자 진료 기록 수정
    def put(self, request, patient_id, medical_record_id):
        if request.user.is_authenticated and request.user.is_practitioner:
            patient = get_object_or_404(Patient, pk=patient_id)
            medical_record = patient.medicalrecord_set.get(
                pk=medical_record_id)
            serializer = MedicalRecordSerializer(
                instance=medical_record, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

class ProcedureRecordAPIView(APIView):
    # 수술 기록 데이터 생성
    def post(self, request):
        if request.user.is_authenticated and request.user.is_practitioner:
            serializer = ProcedureRecordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, procedure_record_id):
        procedure_record = get_object_or_404(
            ProcedureRecord, pk=procedure_record_id)
        serializer = ProcedureRecordSerializer(instance=procedure_record)
        return Response(data=serializer.data)

    def put(self, request, procedure_record_id):
        if request.user.is_authenticated and request.user.is_practitioner:
            procedure_record = get_object_or_404(
                ProcedureRecord, pk=procedure_record_id)
            serializer = ProcedureRecordSerializer(
                instance=procedure_record, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


class ProcedureRecordListAPIView(APIView):
    def get(self, request, medical_record_id):
        procedure_records = ProcedureRecord.objects.filter(
            medical_record=medical_record_id)
        serializer = ProcedureRecordSerializer(
            instance=procedure_records, many=True)
        return Response(data=serializer.data)
