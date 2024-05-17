from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Annual, Schedule
from .serializers import AnnualSerializer
from django.utils.dateparse import parse_date


# Create your views here.


# 연차신청

class MedicalScheduleAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            serializer = AnnualSerializer(data=request.data)
            if serializer.is_valid():
                practitioner = request.user.practitioner
                start_date = serializer.validated_data['start_date']
                end_date = serializer.validated_data['end_date']
                reason = serializer.validated_data.get('reason', '')
                annual = Annual.objects.create(
                    practitioner=practitioner, start_date=start_date,end_date=end_date,reason=reason)
                return Response({"message": "연차 신청이 완료되었습니다."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 사용자가 로그인하지 않았거나 의사가 아닌 경우
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 연차 조회

    def get(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            practitioner = request.user.practitioner
            annuals = Annual.objects.filter(practitioner=practitioner)
            serializer = AnnualSerializer(annuals, many=True)
            return Response(serializer.data)
        else:
            # 사용자가 로그인하지 않았거나 의사가 아닌 경우
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)


class SpecificScheduleAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            practitioner = request.user.practitioner
            
            # 시작 날짜와 끝 날짜 가져오기
            start_date_str = request.data.get('start_date')
            end_date_str = request.data.get('end_date')

            # 시작 날짜와 끝 날짜가 없으면 에러 반환
            if not start_date_str or not end_date_str:
                return Response({"message": "시작 날짜와 끝 날짜를 지정해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # 문자열을 datetime 객체로 변환
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"message": "올바른 날짜 형식이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
                    
            # 연차 조회
            annuals = Annual.objects.filter(
                practitioner=practitioner, 
                start_date__lte=end_date, 
                end_date__gte=start_date
            )
            
            # 시리얼라이저를 통해 JSON 형식으로 변환하여 응답 반환
            serializer = AnnualSerializer(annuals, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)