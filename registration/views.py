from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Patient, RelatedPerson, Account, HumanName
from account.serializers import PatientSerializer, RelatedPersonSerializer


class PatientAPIView(APIView):
    # 환자 데이터 생성
    def post(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            serializer = PatientSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 환자 데이터 조회
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        account = get_object_or_404(Account, pk=patient.account.id)
        if request.user.is_authenticated and (request.user.is_practitioner or request.user == account):
            serializer = PatientSerializer(instance=patient)
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 환자 데이터 수정
    def put(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        account = get_object_or_404(Account, pk=patient.account.id)
        if request.user.is_authenticated and (request.user.is_practitioner or request.user == account):
            serializer = PatientSerializer(
                instance=patient, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


class RelatedPersonAPIView(APIView):
    # 환자 관계자 조회
    def get(self, request, patient_id):
        if request.user.is_authenticated and request.user.is_practitioner():
            patient = get_object_or_404(Patient, pk=patient_id)
            related_persons = patient.relatedperson_set.all()
            if not related_persons:
                return Response({"detail": "환자 관계자가 없습니다."})
            serializer = RelatedPersonSerializer(
                instance=related_persons, many=True)
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 환자 관계자 생성
    def post(self, request, patient_id):
        if request.user.is_authenticated and request.user.is_practitioner():
            patient = get_object_or_404(Patient, pk=patient_id)
            request.data["patient"] = patient.id
            serializer = RelatedPersonSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 환자 관계자 수정
    def put(self, request, patient_id, related_person_id):
        if request.user.is_authenticated and request.user.is_practitioner():
            patient = get_object_or_404(Patient, pk=patient_id)
            try:
                related_person = patient.relatedperson_set.get(
                    pk=related_person_id)
            except RelatedPerson.DoesNotExist:
                return Response({"detail": "환자 관계자가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            serializer = RelatedPersonSerializer(
                data=request.data, instance=related_person, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 환자 관계자 삭제
    def delete(self, request, patient_id, related_person_id):
        if request.user.is_authenticated and request.user.is_practitioner():
            patient = get_object_or_404(Patient, pk=patient_id)
            try:
                related_person = patient.relatedperson_set.get(
                    pk=related_person_id)
            except RelatedPerson.DoesNotExist:
                return Response({"detail": "환자 관계자가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            related_person.delete()
            return Response({"detail": "환자 관계자 정보 삭제 성공"})
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


class PatientSearchAPIView(APIView):
    # 이름, 연락처로 환자 데이터 조회
    def get(self, request):
        if request.user.is_authenticated and request.user.is_practitioner():
            name = request.GET.get('name')
            telecom = request.GET.get('telecom')
            if name:
                patients = Patient.objects.filter(name__name__icontains=name)
                serializer = PatientSerializer(instance=patients, many=True)
                return Response(serializer.data)
            if telecom:
                patients = Patient.objects.filter(telecom__value__icontains=telecom)
                serializer = PatientSerializer(instance=patients, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail": "이름이나 연락처를 제공해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "사용 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)