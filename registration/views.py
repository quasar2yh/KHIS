from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Patient
from account.serializers import PatientSerializer, RelatedPersonSerializer
    
class PatientAPIView(APIView):
    # 환자 데이터 생성
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 환자 데이터 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        serializer = PatientSerializer(patient)
        return Response(data=serializer.data)

    # 환자 데이터 수정
    def put(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)


class RelatedPersonAPIView(APIView):
    # 환자 관계자 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        related_persons = patient.relatedperson_set.all()
        if not related_persons:
            return Response({"detail": "환자 관계자가 없습니다."})
        serializer = RelatedPersonSerializer(data=related_persons, many=True)
        return Response(data=serializer.data)
    
    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        request.data["patient"] = patient.id
        serializer = RelatedPersonSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)