from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Annual, Schedule
from .serializers import AnnualSerializer

# Create your views here.


# 연차 조회
class ScheduleListAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response('111')


# 연차신청
class ScheduleDetailAPIView(APIView):
    def post(self, request, medical_id):
        if request.user.is_authenticated:
            serializer = AnnualSerializer(data=request.data)
            if serializer.is_valid():
                practitioner_id = request.user.id
                date = serializer.validated_data['date']
                annual = Annual.objects.create(
                    practitioner_id=practitioner_id, date=date)
                return Response({"message": "연차 신청이 완료되었습니다."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 사용자가 로그인하지 않은 경우
            return Response({"message": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
