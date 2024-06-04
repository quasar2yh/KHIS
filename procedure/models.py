from django.db import models

# Create your models here.
# 수술
class Procedure(models.Model):
    # 수술 코드
    procedure_code = models.CharField(max_length=30)
    # 수술 이름
    procedure_name = models.CharField(max_length=30)
    # 상세 설명
    description = models.TextField()