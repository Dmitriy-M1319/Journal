from django.db import models
from users.models import TeacherProfile, Platoon


# Модель предмета
class Subject(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    hours_count = models.IntegerField()
    form = models.CharField(max_length=15)

    class Meta:
        db_table = 'subjects'


class SubjectClass(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.DO_NOTHING)
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    class_date = models.DateTimeField()
    theme_number = models.IntegerField()
    theme_name = models.CharField(max_length=255)
    class_number = models.IntegerField()
    class_name = models.CharField(max_length=255)
    class_type = models.CharField(max_length=30)
    classroom = models.IntegerField()

    class Meta:
        db_table = 'subject_classes'
