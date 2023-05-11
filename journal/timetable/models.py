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

    class Meta:
        db_table = 'subjects'

    def json(self):
        return {'id': self.id,
                'teacher': self.teacher.json(),
                'name': self.name,
                'hours_count': self.hours_count,
                'form': self.form
                }


# Модель занятия
class SubjectClass(models.Model):
    # Предмет, по которому было занятие
    subject = models.ForeignKey(Subject, on_delete = models.DO_NOTHING)
    # Взвод, у которого должно быть занятие
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    # Дата и время занятия
    class_date = models.DateTimeField()
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

    class Meta:
        db_table = 'subject_classes'

    def json(self):
        return {'id': self.id,
                'subject': self.subject.json(),
                'platoon': self.platoon.json(),
                'date': self.class_date,
                'theme_number': self.theme_number,
                'theme_name': self.theme_name,
                'class_number': self.class_number,
                'class_name': self.class_name,
                'class_type': self.class_type,
                'classroom': self.classroom
                }
 

