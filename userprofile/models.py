from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from .utils import encrypt_password

# Create your models here.


class UserProfile(AbstractUser):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="male", verbose_name="性别")
    mobile = models.CharField(max_length=11, blank=True, unique=True, verbose_name="电话")
    email = models.EmailField(max_length=64, blank=True, unique=True, verbose_name="邮箱")
    
    class Meta:
        db_table="UserProfile"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
