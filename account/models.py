from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django_cryptography.fields import encrypt
# Create your models here.


class User(AbstractUser):
    CATEGORY_CHOICES = (
        ("남", "남"),
        ("여", "여"),
    )
    LICENSE_CHOICES = (
        ("한의사", "한의사"),
        ("치과", "치과"),
        ("의사", "의사"),
        ("간호사", "간호사"),
    )
    # 이메일 중복허용x Emailvalidator로 유효성검사
    email = models.EmailField(
        max_length=255, unique=True, validators=[EmailValidator()])
    name = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    telecom = models.IntegerField(default=0)
    address = models.IntegerField(default=0)
    encrypted_rrn = encrypt(models.CharField(max_length=100))  # 주민번호 암호화

    # 의료인 면허종별,면허 번호
    license_type = models.CharField(max_length=4, choices=LICENSE_CHOICES)
    license_number = models.CharField(max_length=50)
