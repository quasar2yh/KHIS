from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer, PatientSerializer, PractitionerSerializer, ChangePasswordSerializer
from .models import Account
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class AccountSiginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        account_serializer = AccountSerializer(data=request.data)

        if account_serializer.is_valid(raise_exception=True):
            subject = account_serializer.validated_data["subject"]

            if subject == "Patient":
                patient_serializer = PatientSerializer(data=request.data)

                if patient_serializer.is_valid(raise_exception=True):
                    patient = patient_serializer.save()
                    account_serializer.save(patient=patient)
                    return Response(patient_serializer.data, status=status.HTTP_201_CREATED)

            elif subject == "Practitioner":
                practitioner_serializer = PractitionerSerializer(
                    data=request.data)

                if practitioner_serializer.is_valid(raise_exception=True):
                    practitioner = practitioner_serializer.save()
                    account_serializer.save(practitioner=practitioner)
                    return Response(practitioner_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, account_id):
        account = get_object_or_404(Account, pk=account_id)
        if not request.user.is_authenticated and request.user != account:
            return Response({"detail": "권한 없음"}, status=status.HTTP_400_BAD_REQUEST)
        serailizer = AccountSerializer(instance=account)
        return Response(serailizer.data)

    def put(self, request, account_id):
        account = get_object_or_404(Account, pk=account_id)
        if request.user.is_authenticated and request.user == account:
            account_serializer = AccountSerializer(
                instance=account, data=request.data, partial=True)
            if account_serializer.is_valid(raise_exception=True):
                account_serializer.save()
                return Response(account_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "권한 없음"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, account_id):
        account = get_object_or_404(Account, pk=account_id)
        if request.user.is_authenticated and request.user == account:
            account.delete()
            return Response({"detail": "회원탈퇴 성공"})
        else:
            return Response({"detail": "권한 없음"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    def put(self, request, account_id):
        account = get_object_or_404(Account, pk=account_id)
        if not request.user.is_authenticated and request.user != account:
            return Response({"detail": "권한 없음"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            account.set_password(request.data['new_password'])
            account.save()
        return Response({"detail": "비밀번호 변경 성공"}, status=status.HTTP_200_OK)


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14

            response.set_cookie(
                key='refresh',
                value=response.data['refresh'],
                max_age=cookie_max_age,
                httponly=True,
                samesite='none',
                secure=True
            )

        del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        print(f"\n\n\n\n{request.COOKIES}\n\n\n\n")
        serializer = self.get_serializer(data={"refresh": request.COOKIES.get("refresh")})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        response = Response(serializer.validated_data)

        response.set_cookie(
            key="refresh",
            value=serializer.validated_data.get("refresh"),
            httponly=True,
            max_age=3600 * 24 * 14,
            samesite='none',
            secure=True
        )
        print(f"\n\n\n\n serializer : {serializer.validated_data}\n\n\n")
        del response.data['refresh']
        return response


class LogoutApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({
            "message": "Logout success"
        }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
