"""
Модели пользователей в веб-приложении электронного журнала
"""
from django.db import models
from django.contrib.auth.models import User


class UserData:
    """
    Абстрактный класс данных пользователя
    """
    patronymic = models.CharField(max_length=40)
    military_post = models.CharField(max_length=255)


class TeacherProfile(models.Model, UserData):
    """
    Модель профиля преподавателя на кафедре
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    military_rank = models.CharField(max_length=20)
    cycle = models.CharField(max_length=255)
    teacher_role = models.IntegerField(null=True)
    status = models.CharField(max_length=30)


class Platoon(models.Model):
    """
    Модель взвода на кафедре
    """
    platoon_number = models.IntegerField(primary_key=True)
    tutor = models.OneToOneField(User, on_delete = models.DO_NOTHING)
    year = models.IntegerField(null=True)
    status = models.CharField(max_length=15)

    class Meta:
        db_table = 'platoons'


class StudentProfile(models.Model, UserData):
    """
    Модель профиля студента на кафедре
    """
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    department = models.CharField(max_length=255)
    group_number = models.IntegerField(null=True)
    active = models.CharField(max_length=30)
