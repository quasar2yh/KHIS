from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import ProcedureFee
from .serializers import ProcedureFeeSerializer

class ProcedureFeeAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny
    paginator = PageNumberPagination()

    # 수술 비용 데이터 생성
    # TODO 동일 일, 동일 수술에 대해 중복 요금 작성 방지
    def post(self, request):
        serializer = ProcedureFeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 수술 비용 데이터 조회
    def get(self, request):
        procedure = ProcedureFee.objects.all().order_by('procedure', 'effective_start')
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

