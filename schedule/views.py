from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Annual, Schedule
from .serializers import AnnualSerializer

# Create your views here.


# 연차신청 및 조회

class MedicalScheduleAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            serializer = AnnualSerializer(data=request.data)
            if serializer.is_valid():
                practitioner = request.user.practitioner
                date = serializer.validated_data['date']
                annual = Annual.objects.create(
                    practitioner=practitioner, date=date)
                return Response({"message": "연차 신청이 완료되었습니다."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 사용자가 로그인하지 않았거나 의사가 아닌 경우
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            practitioner = request.user.practitioner
            annuals = Annual.objects.filter(practitioner=practitioner)
            serializer = AnnualSerializer(annuals, many=True)
            return Response(serializer.data)
        else:
            # 사용자가 로그인하지 않았거나 의사가 아닌 경우
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 연차 상세 조회, 수정 및 삭제


# class MedicalScheduleDetailAPIView(APIView):
#     def get(self, request, medical_id):

#     def put(self, request, medical_id):

#     def delete(self, request, medical_id):
        