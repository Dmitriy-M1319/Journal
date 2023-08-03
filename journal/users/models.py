"""
Модели пользователей в веб-приложении электронного журнала
"""
from django.db import models
from django.contrib.auth.models import User


class TeacherProfile(models.Model):
    """
    Модель профиля преподавателя на кафедре
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=40)
    military_post = models.CharField(max_length=255)
    military_rank = models.CharField(max_length=20)
    cycle = models.CharField(max_length=255)
    teacher_role = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default='работает')

    class Meta:
        db_table = 'teachers'


class CourseDirection(models.Model):
    """
    Модель направления и курса для взвода
    """
    course = models.IntegerField()
    direction = models.CharField(max_length=255)

    class Meta:
        db_table = 'course_directions'

 
class Platoon(models.Model):
    """
    Модель взвода на кафедре
    """
    platoon_number = models.IntegerField(primary_key=True)
    tutor = models.OneToOneField(TeacherProfile, on_delete = models.DO_NOTHING)
    year = models.IntegerField(null=True)
    order_of_enrollment = models.CharField(max_length=255, default="")
    status = models.CharField(max_length=15)
    course = models.ForeignKey(CourseDirection, on_delete=models.DO_NOTHING, null=True)
    study_day = models.IntegerField();

    class Meta:
        db_table = 'platoons'


class StudentProfile(models.Model):
    """
    Модель профиля студента на кафедре
    """
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    birth_year = models.IntegerField(default=0)
    patronymic = models.CharField(max_length=40)
    military_post = models.CharField(max_length=255, default='студент')
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    department = models.CharField(max_length=255, default="")
    group_number = models.IntegerField(null=True)
    order_of_expulsion = models.CharField(max_length=255, default="")
    marital_status = models.CharField(max_length=30,default="")
    address = models.CharField(max_length=255,default="")
    phone_number = models.CharField(max_length=11,default="")
    public_load = models.CharField(max_length=50,default="")
    sports_category = models.CharField(max_length=100, default="нет")
    active = models.CharField(max_length=30, default='учится')

    class Meta:
        db_table = 'students'

