from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import Patient, Practitioner, HumanName, RelatedPerson, ContactPoint, Address, Department, CommonInfo, Account


class AccountSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def get_first_name(self, obj):
        if obj.patient and obj.patient.name:
            return obj.patient.name.name
        elif obj.practitioner and obj.practitioner.name:
            return obj.practitioner.name.name
        return None

    def get_last_name(self, obj):
        if obj.patient and obj.patient.name:
            return obj.patient.name.family
        elif obj.practitioner and obj.practitioner.name:
            return obj.practitioner.name.family
        return None

    def save(self, **kwargs):
        password = self.validated_data.get('password', None)
        self.validated_data['password'] = make_password(password)
        return super().save(**kwargs)

    def validate(self, attrs):
        password = attrs.pop('password')
        confirm_password = attrs.pop('confirm_password')
        if password:
            if password != confirm_password:
                raise serializers.ValidationError("비밀번호가 서로 일치하지 않습니다.")
            validate_password(password)
        return super().validate(attrs)


class ContactPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPoint
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['use', 'text', 'city', 'postal_code', 'country']


class HumanNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanName
        fields = '__all__'


class CommonInfoSerializer(serializers.ModelSerializer):
    name = HumanNameSerializer()
    telecom = ContactPointSerializer()
    address = AddressSerializer(required=False)

    class Meta:
        model = CommonInfo
        fields = '__all__'

    def create(self, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)

        name = HumanName.objects.create(**name_data) if name_data else None
        telecom = ContactPoint.objects.create(
            **telecom_data) if telecom_data else None
        address = Address.objects.create(
            **address_data) if address_data else None

        return {
            'name': name,
            'telecom': telecom,
            'address': address,
        }

    def update(self, instance, validated_data):
        name_data = validated_data.pop('name', None)
        telecom_data = validated_data.pop('telecom', None)
        address_data = validated_data.pop('address', None)

        if name_data:
            if instance.name:
                name_serializer = HumanNameSerializer(
                    instance.name, data=name_data, partial=True)
                if name_serializer.is_valid():
                    name_serializer.save()
            else:
                instance.name = HumanName.objects.create(**name_data)

        if telecom_data:
            if instance.telecom:
                telecom_serializer = ContactPointSerializer(
                    instance.telecom, data=telecom_data, partial=True)
                if telecom_serializer.is_valid():
                    telecom_serializer.save()
            else:
                instance.telecom = ContactPoint.objects.create(**telecom_data)

        if address_data:
            if instance.address:
                address_serializer = AddressSerializer(
                    instance.address, data=address_data, partial=True)
                if address_serializer.is_valid():
                    address_serializer.save()
            else:
                instance.address = Address.objects.create(**address_data)

        instance = super().update(instance, validated_data)

        instance.save()
        return instance


class RelatedPersonSerializer(CommonInfoSerializer):
    class Meta:
        model = RelatedPerson
        fields = '__all__'

    def create(self, validated_data):
        common_info = super().create(validated_data)
        related_person = RelatedPerson.objects.create(
            name=common_info['name'], telecom=common_info['telecom'], address=common_info['address'], **validated_data)

        return related_person


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PatientSerializer(CommonInfoSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        common_info = super().create(validated_data)
        patient = Patient.objects.create(
            name=common_info['name'], telecom=common_info['telecom'], address=common_info['address'], **validated_data)

        return patient


class PractitionerSerializer(CommonInfoSerializer):

    class Meta:
        model = Practitioner
        fields = '__all__'

    def create(self, validated_data):
        common_info = super().create(validated_data)
        department_data = validated_data.pop('department', None)
        practitioner = Practitioner.objects.create(
            name=common_info['name'], telecom=common_info['telecom'], address=common_info['address'], **validated_data)

        if department_data:
            practitioner.department = department_data
            practitioner.save()
        return practitioner

    def update(self, instance, validated_data):
        department_data = validated_data.pop('department', None)

        if department_data:
            instance.department = department_data
            instance.save()

        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context['request'].user
        old_password = data.pop('old_password', None)
        new_password = data.get('new_password')
        confirm_password = data.pop('confirm_password', None)

        if not user.check_password(old_password):
            raise serializers.ValidationError("현재 비밀번호가 일치하지 않습니다.")
        if not new_password:
            raise serializers.ValidationError("새 비밀번호를 입력해주세요.")
        if new_password != confirm_password:
            raise serializers.ValidationError("비밀번호가 서로 일치하지 않습니다.")
        if user.check_password(new_password):
            raise serializers.ValidationError("새 비밀번호가 현재 비밀번호와 같습니다.")
        validate_password(new_password)
        return data


