from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, MedicalUserSerializer
from .models import User
from django.contrib.auth.hashers import check_password
# Create your views here.


class AccountSiginAPIView(APIView):  # 일반회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MedicalSiginAPIView(APIView):  # 메티컬 회원가입
    def post(self, request):
        serializer = MedicalUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountLogoutAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):  # 로그아웃
        refresh_token = request.data.get("refresh_token")
        if refresh_token is None:
            print("로그아웃 실패: refresh_token이 제공되지 않음")
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("로그아웃 성공")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountProfileAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def put(self, request, username):  # 일반유저 정보수정
        user = get_object_or_404(User, username=username)
        if user.username == username:
            serializer = UserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, username):  # 회원탈퇴
        user = get_object_or_404(User, username=username)
        password = request.data.get('password')
        if check_password(password, user.password):
            user.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
