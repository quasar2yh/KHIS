from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from account.models import Patient
from .models import Procedure, ProcedureRecord, ProcedureFee
from .serializers import (
    MedicalRecordSerializer, ProcedureSerializer, ProcedureRecordSerializer,
    ProcedureFeeSerializer)


class MedicalRecordAPIView(APIView):
    # 환자 진료 기록 생성
    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

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
        patient = get_object_or_404(Patient, pk=patient_id)
        medical_record = patient.medicalrecord_set.get(
            pk=medical_record_id)
        serializer = MedicalRecordSerializer(
            instance=medical_record, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)


class ProcedureAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny
    paginator = PageNumberPagination()

    # 수술 데이터 생성
    def post(self, request):
        serializer = ProcedureSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 수술 데이터 조회
    def get(self, request):
        procedure = Procedure.objects.all()
        page = self.paginator.paginate_queryset(
            procedure, request, view=self)
        serializer = ProcedureSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ProcedureDetailAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny

    # 수술 데이터 수정
    def put(self, request, procedure_id):
        procedure = get_object_or_404(Procedure, pk=procedure_id)
        serializer = ProcedureSerializer(
            procedure, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 수술 데이터 상세 조회
    def get(self, request, procedure_id):
        procedure = get_object_or_404(Procedure, pk=procedure_id)
        serializer = ProcedureSerializer(instance=procedure)
        return Response(data=serializer.data)
    
    # 수술 데이터 삭제
    def delete(self, request, procedure_id):
        procedure = get_object_or_404(Procedure, pk=procedure_id)
        serializer = ProcedureSerializer(instance=procedure)
        if serializer.is_valid():
            serializer.delete()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProcedureRecordAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny

    # 수술 기록 데이터 생성
    def post(self, request):
        serializer = ProcedureRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    def get(self, request, procedure_record_id):
        procedure_record = get_object_or_404(
            ProcedureRecord, pk=procedure_record_id)
        serializer = ProcedureRecordSerializer(instance=procedure_record)
        return Response(data=serializer.data)

    def put(self, request, procedure_record_id):
        procedure_record = get_object_or_404(
            ProcedureRecord, pk=procedure_record_id)
        serializer = ProcedureRecordSerializer(
            instance=procedure_record, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)


class ProcedureFeeAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny
    paginator = PageNumberPagination()

    # 수술 비용 데이터 생성
    def post(self, request):
        serializer = ProcedureFeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 수술 비용 데이터 조회
    def get(self, request):
        procedure = ProcedureFee.objects.all()
        page = self.paginator.paginate_queryset(
            procedure, request, view=self)
        serializer = ProcedureFeeSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ProcedureFeeDetailAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny

    # 수술 비용 데이터 수정
    def put(self, request, procedurefee_id):
        procedure_fee = get_object_or_404(ProcedureFee, pk=procedurefee_id)
        serializer = ProcedureFeeSerializer(
            procedure_fee, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 수술 비용 데이터 상세 조회
    def get(self, request, procedurefee_id):
        procedure_fee = get_object_or_404(ProcedureFee, pk=procedurefee_id)
        serializer = ProcedureFeeSerializer(procedure_fee)
        return Response(data=serializer.data)
