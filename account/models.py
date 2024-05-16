from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Unknown', 'Unknown'),
    ]


class Account(AbstractUser):
    SUBJECT_CHOICES = [
        ("Patient", 'Patient'),
        ("Practitioner", 'Practitioner')
    ]
    subject = models.CharField(max_length=20)
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE, blank=True, null=True)
    practitioner = models.OneToOneField('Practitioner', on_delete=models.CASCADE, blank=True, null=True)


class Patient(models.Model):

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

    name = models.ForeignKey('HumanName', on_delete=models.CASCADE, blank=True, null=True)
    telecom = models.ForeignKey('ContactPoint', on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateTimeField()
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, null=True)
    blood_type = models.CharField(max_length=10, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)
    related_person = models.ForeignKey('RelatedPerson', on_delete=models.CASCADE, blank=True, null=True)
    # 환자 관계자, 보호자
    marital_status = models.BooleanField(blank=True)
    # 환자의 결혼 여부 True | False
    allergies = models.CharField(max_length=255, blank=True)
    # 환자의 여부 ex) 땅콩, 복숭아 ...
    medical_record = models.ForeignKey('MedicalRecord', on_delete=models.CASCADE, blank=True, null=True)
    # 환자의 진료 기록
    

class Practitioner(models.Model):

    ROLE_CHOICES = [
        ('Physician', 'Physician'),
        ('Assistant', 'Assistant'),
    ]

    name = models.ForeignKey('HumanName', on_delete=models.CASCADE, blank=True, null=True)
    telecom = models.ForeignKey('ContactPoint', on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, blank=True, null=True)
    # 해당 의료관계자의 부서
    license_type = models.CharField(max_length=10)
    # 자격증 타입
    license_number = models.CharField(max_length=100)
    # 해당 자격증의 번호
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # Physician | Assistant
    rank = models.IntegerField()
    # 권한 레벨 1~3


class RelatedPerson(models.Model):
    name = models.ForeignKey('HumanName', on_delete=models.CASCADE)
    telecom = models.ForeignKey('ContactPoint', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(blank=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True)


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
    value = models.TextField()
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
    department = models.CharField(max_length=100)


class MedicalRecord(models.Model):
    diagnosis = models.TextField()
    # 진단 내용
    diagnostic_results = models.TextField(blank=True)
    # 진단 결과
    surgical_request_record = models.TextField(blank=True)
    # 수술 요청 기록
    surgical_result = models.TextField(blank=True)
    # 수술 결과
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Annual(models.Model):
    # 연차 관련 테이블
    practitioner = models.ForeignKey('Practitioner')
    date = models.DateField()
    # 연차 사용한 날짜


class GeneralPractitioner():
    # 환자와 담당의사 중계 테이블
    patient = models.ForeignKey('Patient')
    practitioner = models.ForeignKey('Practitioner')


class Schedule():
    # 병원 쪽 스케줄
    # ex) 병원 휴일, 해당 의사 연차, ...
    department = models.ForeignKey('Department', blank=True, null=True)
    practitioner = models.ForeignKey('Practitioner', blank=True, null=True)
    datetime = models.DateTimeField()


class Appointment():
    # 환자의 예약 데이터
    department = models.ForeignKey('Department')
    patient = models.ForeignKey('Patient')
    practitioner = models.ForeignKey('Practitioner', blank=True, null=True)
    datetime = models.DateTimeField()
    syptom = models.TextField()
    # 증상
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    active = models.BooleanField()