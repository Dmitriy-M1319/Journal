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
    surname = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    patronymic = models.CharField(max_length=40, null=True)
    military_post = models.CharField(max_length=255, null=True)
    military_rank = models.CharField(max_length=20)
    cycle = models.CharField(max_length=255)
    teacher_role = models.IntegerField(null=True)
    status = models.CharField(max_length=30)

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
    status = models.CharField(max_length=15)
    course = models.ForeignKey(CourseDirection, on_delete=models.DO_NOTHING, null=True)
    # День прихода (понедельник - 0, вторник - 1 и т.д.
    study_day = models.IntegerField();
    class Meta:
        db_table = 'platoons'


class StudentProfile(models.Model):
    """
    Модель профиля студента на кафедре
    """
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    surname = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    patronymic = models.CharField(max_length=40, null=True)
    military_post = models.CharField(max_length=255, null=True)
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    department = models.CharField(max_length=255)
    group_number = models.IntegerField(null=True)
    active = models.CharField(max_length=30)

    class Meta:
        db_table = 'students'


