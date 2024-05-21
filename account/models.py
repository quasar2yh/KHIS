from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
    ('Unknown', 'Unknown'),
]


class CommonInfo(models.Model):
    name = models.OneToOneField(
        'HumanName', on_delete=models.CASCADE, blank=True, null=True)
    telecom = models.OneToOneField(
        'ContactPoint', on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateTimeField(blank=True, null=True)
    address = models.OneToOneField(
        'Address', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if self.name:
            self.name.delete()
        if self.telecom:
            self.telecom.delete()
        if self.address:
            self.address.delete()
        return super().delete(*args, **kwargs)

class Account(AbstractUser):
    SUBJECT_CHOICES = [
        ("Patient", 'Patient'),
        ("Practitioner", 'Practitioner')
    ]
    subject = models.CharField(max_length=20)
    patient = models.OneToOneField(
        'Patient', on_delete=models.CASCADE, blank=True, null=True)
    practitioner = models.OneToOneField(
        'Practitioner', on_delete=models.CASCADE, blank=True, null=True)

    def is_practitioner(self):
        return self.subject == 'Practitioner'


class Patient(CommonInfo):

    BLOOD_TYPE_CHOICES = [
        ('RH+A', 'RH+A'),
        ('RH-A', 'RH-A'),
        ('RH+B', 'RH+B'),
        ('RH-B', 'RH-B'),
        ('RH+O', 'RH+O'),
        ('RH-O', 'RH-O'),
        ('RH+AB', 'RH+AB'),
        ('RB-AB', 'RB-AB')
    ]

    blood_type = models.CharField(
        max_length=10, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)
    marital_status = models.BooleanField(blank=True)
    # 환자의 결혼 여부 True | False
    allergies = models.CharField(max_length=255, blank=True)
    # 환자의 여부 ex) 땅콩, 복숭아 ...


class Practitioner(CommonInfo):

    ROLE_CHOICES = [
        ('Physician', 'Physician'),
        ('Assistant', 'Assistant'),
    ]

    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, blank=True, null=True)
    # 해당 의료관계자의 부서
    license_type = models.CharField(max_length=10)
    # 자격증 타입
    license_number = models.CharField(max_length=100)
    # 해당 자격증의 번호
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # Physician | Assistant
    rank = models.IntegerField()
    # 권한 레벨 1~3

    def delete(self, *args, **kwargs):
        if self.department:
            self.department.delete()
        return super().delete(*args, **kwargs)

class RelatedPerson(CommonInfo):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)


class HumanName(models.Model):
    name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)


class ContactPoint(models.Model):
    SYSTEM_CHOICES = [
        ('Phone', 'Phone'),
        ('Fax', 'Fax'),
        ('Email', 'Email'),
        ('Pager', 'Pager'),
        ('URL', 'URL'),
        ('SMS', 'SMS'),
        ('Other', 'Other'),
    ]

    USE_CHOICES = [
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Temp', 'Temp'),
        ('Old', 'Old'),
        ('Mobile', 'Mobile'),
    ]

    system = models.CharField(max_length=10, choices=SYSTEM_CHOICES)
    value = models.TextField(unique=True)
    use = models.CharField(max_length=10, choices=USE_CHOICES)


class Address(models.Model):
    USE_CHOICES = [
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Temp', 'Temp'),
        ('Old', 'Old'),
        ('Billing', 'Billing'),
    ]

    use = models.CharField(max_length=10, choices=USE_CHOICES)
    text = models.TextField()
    # 실제 주소 값
    # 서울시 무슨구 어디길 ...
    city = models.CharField(max_length=100)
    # ex) 서울시, 강릉시 ...
    postal_code = models.CharField(max_length=20)
    # 우편번호 ex) 25583
    country = models.CharField(max_length=100)
    # 국가 ex) SouthKorea


class Department(models.Model):
    DEPARTMENT = [
        ('치과', '치과'),
        ('내과', '내과'),
        ('안과', '안과'),
        ('외과', '외과'),
    ]

    department = models.CharField(max_length=10, choices=DEPARTMENT)


class GeneralPractitioner():
    # 환자와 담당의사 중계 테이블
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    practitioner = models.ForeignKey('Practitioner', on_delete=models.CASCADE)
