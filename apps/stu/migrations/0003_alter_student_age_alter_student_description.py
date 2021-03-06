# Generated by Django 4.0.6 on 2022-07-13 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu', '0002_remove_student_sex_student_birthday_student_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='student',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='学生简介'),
        ),
    ]
