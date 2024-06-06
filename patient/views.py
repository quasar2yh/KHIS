from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import Account


class ChargeItemAPIView(APIView):
    permission_classes = [AllowAny]  # 테스트용 AllowAny

    def get(self):
        return Response(" ")
    
    def post(self, request, patient_id):
        if Account.objects.get(patient_id=patient_id).exists():
            return Response({"message": "환자 존재"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "환자 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self):
        return " "
    
    def delete(self):
        return " "








