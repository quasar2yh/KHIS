from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Practitioner
from account.serializers import PractitionerSerializer


class PractitionerAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            serializer = PractitionerSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, practitioner_id):
        if request.user.is_authenticated and request.user.is_practitioner:
            practitioner = get_object_or_404(Practitioner, pk=practitioner_id)
            serializer = PractitionerSerializer(instance=practitioner)
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, practitioner_id):
        if request.user.is_authenticated and request.user.is_practitioner:
            practitioner = get_object_or_404(Practitioner, pk=practitioner_id)
            serializer = PractitionerSerializer(
                instance=practitioner, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
