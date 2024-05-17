from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Patient, RelatedPerson
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
        serializer = PatientSerializer(instance=patient)
        return Response(data=serializer.data)

    # 환자 데이터 수정
    def put(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        serializer = PatientSerializer(instance=patient, data=request.data, partial=True)
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
        serializer = RelatedPersonSerializer(instance=related_persons, many=True)
        return Response(data=serializer.data)
    
    # 환자 관계자 생성
    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        request.data["patient"] = patient.id
        serializer = RelatedPersonSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)
    
    # 환자 관계자 수정
    def put(self, requset, patient_id, related_person_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        try:
            related_person = patient.relatedperson_set.get(pk=related_person_id)
        except RelatedPerson.DoesNotExist:
            return Response({"detail":"환자 관계자가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RelatedPersonSerializer(data=requset.data, instance=related_person, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

    # 환자 관계자 삭제
    def delete(self, request, patient_id, related_person_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        try:
            related_person = patient.relatedperson_set.get(pk=related_person_id)
        except RelatedPerson.DoesNotExist:
            return Response({"detail":"환자 관계자가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        related_person.delete()
        return Response({"detail":"환자 관계자 정보 삭제 성공"})
        