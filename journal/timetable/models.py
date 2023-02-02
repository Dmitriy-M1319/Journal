from django.db import models
from users.models import Teacher, Platoon


# Модель предмета
class Subject(models.Model):
    # Преподаватель (ссылка на преподавателя)
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    # Название предмета
    name = models.CharField(max_length=100)
    # Количество часов
    hours_count = models.IntegerField()
    # Форма отчетности (экзамен, зачет)
    form = models.CharField(max_length=15)


# Модель занятия
class SubjectClass(models.Model):
    # Предмет, по которому было занятие
    subject = models.ForeignKey(Subject, on_delete = models.DO_NOTHING)
    # Взвод, у которого должно быть занятие
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    # Дата занятия
    date = models.DateField()
    # Номер темы
    theme_number = models.IntegerField()
    # Название темы
    theme_name = models.CharField(max_length=255)
    # Номер занятия
    class_number = models.IntegerField()
    # Название занятия
    class_name = models.CharField(max_length=255)
    # Тип занятия (лекция, семинар, контрольное занятие)
    class_type = models.CharField(max_length=30)
    # Номер аудитории
    classroom = models.IntegerField()

