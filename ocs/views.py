from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from account.models import Patient
from account.serializers import PatientSerializer

@api_view(["POST"])
def patient_create(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(data=serializer.data)

