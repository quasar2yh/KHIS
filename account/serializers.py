from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Patient, Practitioner, HumanName, RelatedPerson, ContactPoint, Address, Department


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


class RelatedPersonSerializer(serializers.ModelSerializer):
    name = HumanNameSerializer()
    telecom = ContactPointSerializer()
    address = AddressSerializer(required=False)

    class Meta:
        model = RelatedPerson
        fields = '__all__'

    def create(self, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)

        name = HumanName.objects.create(**name_data)
        telecom = ContactPoint.objects.create(**telecom_data)
        address = Address.objects.create(
            **address_data) if address_data else None

        related_person = RelatedPerson.objects.create(
            name=name, telecom=telecom, address=address, **validated_data)
        return related_person

    def update(self, instance, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)

        instance = super().update(instance, validated_data)

        if name_data:
            name_serializer = HumanNameSerializer(
                instance.name, data=name_data)
            if name_serializer.is_valid():
                name_serializer.save()
        if telecom_data:
            telecom_serializer = ContactPointSerializer(
                instance.telecom, data=telecom_data)
            if telecom_serializer.is_valid():
                telecom_serializer.save()
        if address_data:
            address_serializer = AddressSerializer(
                instance.address, data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()

        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    name = HumanNameSerializer()
    telecom = ContactPointSerializer()
    address = AddressSerializer(required=False)

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)

        name = HumanName.objects.create(**name_data)
        telecom = ContactPoint.objects.create(**telecom_data)
        address = Address.objects.create(
            **address_data) if address_data else None

        patient = Patient.objects.create(
            name=name, telecom=telecom, address=address, **validated_data)
        return patient

    def update(self, instance, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)

        instance = super().update(instance, validated_data)

        if name_data:
            name_serializer = HumanNameSerializer(
                instance.name, data=name_data)
            if name_serializer.is_valid():
                name_serializer.save()
        if telecom_data:
            telecom_serializer = ContactPointSerializer(
                instance.telecom, data=telecom_data)
            if telecom_serializer.is_valid():
                telecom_serializer.save()
        if address_data:
            address_serializer = AddressSerializer(
                instance.address, data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()

        return instance


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

        name = HumanName.objects.create(**name_data)
        telecom = ContactPoint.objects.create(**telecom_data)
        address = Address.objects.create(
            **address_data) if address_data else None
        department = Department.objects.create(
            **department_data) if department_data else None

        practiioner = Practitioner.objects.create(
            name=name, telecom=telecom, address=address, department=department, **validated_data)
        return practiioner

    def update(self, instance, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)
        department_data = validated_data.pop('department', None)

        instance = super().update(instance, validated_data)

        if name_data:
            name_serializer = HumanNameSerializer(
                instance.name, data=name_data)
            if name_serializer.is_valid():
                name_serializer.save()
        if telecom_data:
            telecom_serializer = ContactPointSerializer(
                instance.telecom, data=telecom_data)
            if telecom_serializer.is_valid():
                telecom_serializer.save()
        if address_data:
            address_serializer = AddressSerializer(
                instance.address, data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()
        if department_data:
            department_serializer = DepartmentSerializer(
                instance.department, data=department_data)
            if department_serializer.is_valid():
                department_serializer.save()

        return instance
