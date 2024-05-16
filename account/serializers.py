from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Patient, Practitioner, HumanName, RelatedPerson, ContactPoint, Address, MedicalRecord, Department


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        
    def save(self, **kwargs):
        password = make_password(self.validated_data['password'])
        self.validated_data['password'] = password
        return super().save(**kwargs)


class ContactPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPoint
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class HumanNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanName
        fields = '__all__'


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class RelatedPersonSerializer(serializers.ModelSerializer):
    name = HumanNameSerializer()
    telecom = ContactPointSerializer()
    address = AddressSerializer()
    class Meta:
        model = RelatedPerson
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    name = HumanNameSerializer()
    telecom = ContactPointSerializer()
    address = AddressSerializer(required=False)
    related_person = RelatedPersonSerializer(required=False)
    medical_record = MedicalRecordSerializer(required=False)

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)
        related_person_data = validated_data.pop('related_person', None)
        medical_record_data = validated_data.pop('medical_record', None)

        patient = Patient.objects.create(**validated_data)

        if name_data:
            name = HumanName.objects.create(**name_data)
            patient.name = name
        if telecom_data:
            telecom = ContactPoint.objects.create(**telecom_data)
            patient.telecom = telecom
        if address_data:
            address = Address.objects.create(**address_data)
            patient.address = address
        if related_person_data:
            related_person = RelatedPerson.objects.create(**related_person_data)
            patient.related_person = related_person
        if medical_record_data:
            medical_record = MedicalRecord.objects.create(**medical_record_data)
            patient.medical_record=medical_record

        patient.save()
        return patient


class PractitionerSerializer(serializers.ModelSerializer):
    name = HumanNameSerializer()
    telecom = ContactPointSerializer()
    address = AddressSerializer(required=False)
    department = DepartmentSerializer(required=False)
    class Meta:
        model = Practitioner
        fields = '__all__'

    def create(self, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)
        department_data = validated_data.pop('department', None)

        prectitioner = Practitioner.objects.create(**validated_data)

        if name_data:
            name = HumanName.objects.create(**name_data)
            prectitioner.name = name
        if telecom_data:
            telecom = ContactPoint.objects.create(**telecom_data)
            prectitioner.telecom = telecom
        if address_data:
            address = Address.objects.create(**address_data)
            prectitioner.address = address
        if department_data:
            department = Department.objects.create(**department_data)
            prectitioner.department = department
        
        prectitioner.save()
        return prectitioner