from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'encrypted_rrn', 'password', 'gender',
                  'birth_date', 'telecom', 'address', 'email')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            name=validated_data['name'],
            encrypted_rrn=validated_data['encrypted_rrn'],
            gender=validated_data['gender'],
            birth_date=validated_data['birth_date'],
            telecom=validated_data['telecom'],
            address=validated_data['address'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # 비밀번호 해싱하긔
        user.save()
        return user


class MedicalUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    # def validate_license_number(self, value):
    #     # 면허 번호에 대한 유효성 검증 로직 구현
    #
    #     return value

    def create(self, validated_data):
        user = super().create(validated_data)
        user.license_type = validated_data['license_type']
        user.license_number = validated_data['license_number']
        user.save()
        return user


class UserupdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'name', 'encrypted_rrn', 'password', 'gender',
                  'birth_date', 'telecom', 'address', 'email')


class MedicalUserupdateSerializer(serializers.ModelSerializer):
    model = User
    fields = "__all__"
