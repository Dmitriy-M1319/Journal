from django.db import models
from users.models import Student
from timetable.models import SubjectClass

# Модель журнальной записи (клеточка в обычном журнале)

class JournalCeil(models.Model):
    # Студент, которому принадлежит клеточка
    student = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
    # Занятие, за которое ставится оценка
    subject_class = models.ForeignKey(SubjectClass, on_delete = models.DO_NOTHING)
    # Оценка
    mark = models.IntegerField()
    # Посещаемость (был, неуваж. причина, болен)
    attendance = models.CharField(max_length=10)
    # Оставим место для справки в случае болезни



