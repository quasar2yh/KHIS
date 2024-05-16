from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer, PatientSerializer, PractitionerSerializer


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
                    account_serializer.save(patient = patient)
                    return Response(patient_serializer.data, status=status.HTTP_201_CREATED)
                
            elif subject == "Practitioner":
                practitioner_serializer = PractitionerSerializer(data=request.data)

                if practitioner_serializer.is_valid(raise_exception=True):
                    practitioner = practitioner_serializer.save()
                    account_serializer.save(practitioner = practitioner)
                    return Response(practitioner_serializer.data, status=status.HTTP_201_CREATED)
