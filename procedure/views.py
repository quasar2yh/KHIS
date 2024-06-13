from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from account.models import Patient
from .models import Procedure
from .serializers import ProcedureSerializer, ProcedureDetailSerializer


class ProcedureAPIView(APIView):
    paginator = PageNumberPagination()

    # 수술 데이터 생성
    def post(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            serializer = ProcedureSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 환자의 수술 데이터 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        procedures = Procedure.objects.filter(procedurerecord__patient=patient)
        page = self.paginator.paginate_queryset(
            procedures, request, view=self)
        serializer = ProcedureSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ProcedureDetailAPIView(APIView):
    # 수술 데이터 수정
    def put(self, request, procedure_id):
        if request.user.is_authenticated and request.user.is_practitioner():
            procedure = get_object_or_404(Procedure, pk=procedure_id)
            serializer = ProcedureSerializer(
                procedure, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
    # 수술 데이터 상세 조회
    def get(self, request, procedure_id):
        procedure = get_object_or_404(Procedure, pk=procedure_id)
        serializer = ProcedureDetailSerializer(instance=procedure)
        return Response(data=serializer.data)

    # 수술 데이터 삭제
    def delete(self, request, procedure_id):
        if request.user.is_authenticated and request.user.is_practitioner():
            procedure = get_object_or_404(Procedure, pk=procedure_id)
            serializer = ProcedureSerializer(instance=procedure)
            if serializer.is_valid():
                serializer.delete()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

class UnchargedProcedureListAPIView(APIView):
    def get(self, request, patient_id):
        if request.user.is_authenticated and request.user.is_practitioner():
            patient = get_object_or_404(Patient, pk=patient_id)
            procedures = Procedure.objects.filter(
                procedurerecord__patient=patient, charge_items__isnull=True)
            serializer = ProcedureSerializer(procedures, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)