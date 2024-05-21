import requests
import datetime
from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Annual, HospitalSchedule
from .serializers import AnnualSerializer, HospitalScheduleSerializer
from django.utils.dateparse import parse_date
from .utils import sync_schedules_with_holidays, save_holidays_from_api


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
                    practitioner=practitioner, start_date=start_date, end_date=end_date, reason=reason)
                return Response({"message": "연차 신청이 완료되었습니다."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 사용자가 로그인하지 않았거나 의사가 아닌 경우
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 본인 연차 조회

    def get(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            practitioner = request.user.practitioner
            annuals = Annual.objects.filter(practitioner=practitioner)
            serializer = AnnualSerializer(annuals, many=True)
            return Response(serializer.data)
        else:
            # 사용자가 로그인하지 않았거나 의사가 아닌 경우
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 특정 본인 구간연차 조회

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
                start_date = datetime.strptime(
                    start_date_str, '%Y-%m-%d').date()
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


class MedicalIntegratedAPIView(APIView):  # 전체 직원 연차 조회
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_practitioner():
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_403_FORBIDDEN)

        medical_staff_schedules = Annual.objects.all()
        medical_staff_serializer = AnnualSerializer(
            medical_staff_schedules, many=True)
        return Response(medical_staff_serializer.data, status=status.HTTP_200_OK)


class MedicalSpecificIntegratedAPIView(APIView):  # 전체 직원 연차의 구간 조회
    def get(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():

            # 시작 날짜와 끝 날짜 가져오기
            start_date_str = request.data.get('start_date')
            end_date_str = request.data.get('end_date')

            # 시작 날짜와 끝 날짜가 없으면 에러 반환
            if not start_date_str or not end_date_str:
                return Response({"message": "시작 날짜와 끝 날짜를 지정해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # 문자열을 datetime 객체로 변환
                start_date = datetime.strptime(
                    start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"message": "올바른 날짜 형식이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

            # 연차 조회
            annuals = Annual.objects.filter(
                start_date__lte=end_date,
                end_date__gte=start_date
            )

            # 시리얼라이저를 통해 JSON 형식으로 변환하여 응답 반환
            serializer = AnnualSerializer(annuals, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "의사로 로그인해야 합니다."}, status=status.HTTP_401_UNAUTHORIZED)


class HospitalScheduleAPIView(APIView):  # 병원 공휴일 관리
    def post(self, request):
        serializer = HospitalScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # 공휴일 DB저장
        save_holidays_from_api()
        # 공휴일 동기화
        sync_schedules_with_holidays()

        # 모든 공휴일 조회
        schedules = HospitalSchedule.objects.all()

        # 직접 작성한 공휴일과 API에서 가져온 공휴일을 함께 조회
        serializer = HospitalScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


class HospitalScheduleDetailAPIView(APIView):  # 병원 공휴일 수정 및 삭제
    def put(self, request, hospitalschedule_id):
        try:
            schedule = HospitalSchedule.objects.get(id=hospitalschedule_id)
            serializer = HospitalScheduleSerializer(
                schedule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except HospitalSchedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, hospitalschedule_id):
        try:
            schedule = HospitalSchedule.objects.get(id=hospitalschedule_id)
            schedule.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HospitalSchedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class IntegratedScheduleAPIView(APIView):
    def get(self, request):
        # 병원 휴일 조회
        hospital_schedules = HospitalSchedule.objects.all()
        hospital_serializer = HospitalScheduleSerializer(
            hospital_schedules, many=True)

        # 의료진 전체 스케줄 조회
        medical_staff_schedules = Annual.objects.all()
        medical_staff_serializer = AnnualSerializer(
            medical_staff_schedules, many=True)

        # 병원 휴일과 의료진 전체 스케줄을 통합하여 응답
        integrated_data = {
            "hospital_schedules": hospital_serializer.data,
            "medical_staff_schedules": medical_staff_serializer.data
        }
        return Response(integrated_data)
