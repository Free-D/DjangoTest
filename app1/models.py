from django.db import models

# Create your models here.

class Student(models.Model):
    # 模型字段
    name = models.CharField(max_length=100, verbose_name="姓名")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="male", verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    age = models.IntegerField(null=True, blank=True, verbose_name="年龄")
    class_null = models.CharField(max_length=5, verbose_name="班级编号")
    description = models.TextField(null=True, blank=True, max_length=1000, verbose_name="学生简介")

    class Meta:
        db_table="StudentInfo"
        verbose_name = "学生"
        verbose_name_plural = verbose_name

