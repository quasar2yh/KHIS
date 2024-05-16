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
    marital_status = models.BooleanField(blank=True)
    allergies = models.CharField(max_length=255, blank=True)
    medical_record = models.ForeignKey('MedicalRecord', on_delete=models.CASCADE, blank=True, null=True)

    
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
    license_type = models.CharField(max_length=10)
    license_number = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    rank = models.IntegerField()


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
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)


class Department(models.Model):
    department = models.CharField(max_length=100)


class MedicalRecord(models.Model):
    diagnosis = models.TextField()
    diagnostic_results = models.TextField(blank=True)
    surgical_request_record = models.TextField(blank=True)
    surgical_result = models.TextField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()