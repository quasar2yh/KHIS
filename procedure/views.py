from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from account.models import Patient
from acceptance.models import ChargeItem
from .models import Procedure
from .serializers import ProcedureSerializer, ProcedureDetailSerializer


class ProcedureAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny
    paginator = PageNumberPagination()

    # 수술 데이터 생성
    def post(self, request):
        serializer = ProcedureSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 환자의 수술 데이터 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        procedures = Procedure.objects.filter(procedurerecord__patient=patient)
        page = self.paginator.paginate_queryset(
            procedures, request, view=self)
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
        serializer = ProcedureDetailSerializer(instance=procedure)
        return Response(data=serializer.data)

    # 수술 데이터 삭제
    def delete(self, request, procedure_id):
        procedure = get_object_or_404(Procedure, pk=procedure_id)
        serializer = ProcedureSerializer(instance=procedure)
        if serializer.is_valid():
            serializer.delete()
        return Response(data=serializer.data)


class UnchargedProcedureListAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        procedures = Procedure.objects.filter(
            procedurerecord__patient=patient, charge_items__isnull=True)
        serializer = ProcedureSerializer(procedures, many=True)
        return Response(serializer.data)
