"""
    Модели пользователей в веб-приложении электронного журнала
"""
from django.db import models

class Teacher(models.Model):
    """Модель преподавателя на кафедре"""
    # Фамилия
    surname = models.CharField(max_length=40)
    # Имя 
    name = models.CharField(max_length=40)
    # Отчество
    patronymic = models.CharField(max_length=40)
    # Воинское звание
    military_rank = models.CharField(max_length=20)
    # Воинская должность
    military_post = models.CharField(max_length=255)
    # Цикл
    cycle = models.CharField(max_length=255)
    # Роль в системе (обычный преподаватель или суперпользователь)
    role = models.IntegerField()
    # Логин в учетной системе
    login = models.CharField(max_length=30)
    # Пароль (в хэшированном виде)
    password = models.CharField(max_length=255)
    # Статус преподавателя (работает или уволен)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = 'teachers'

    def json(self):
        return {'surname': self.surname, 
                    'name': self.name,
                    'patronymic': self.patronymic,
                    'military_rank': self.military_rank,
                    'military_post': self.military_post,
                    'cycle': self.cycle,
                    'login': self.login,
                    'password': self.password,
                    'status': self.status
                    }


class Platoon(models.Model):
    """Модель взвода на кафедре"""
    # Номер взвода (выступает первичным ключом)
    platoon_number = models.IntegerField(primary_key=True)
    # Куратор взвода (ссылка на преподавателя)
    tutor = models.OneToOneField(Teacher, on_delete = models.DO_NOTHING)
    # Год набора
    year = models.IntegerField()
    # Статус взвода (учится или выпустился)
    status = models.CharField(max_length=15)

    class Meta:
        db_table = 'platoons'

    def json(self):
        return {'number': self.platoon_number,
                    'year': self.year,
                    'tutor': self.tutor.json()
                    }

class Student(models.Model):
    """Модель студента на кафедре"""
    # Фамилия
    surname = models.CharField(max_length=40)
    # Имя 
    name = models.CharField(max_length=40)
    # Отчество
    patronymic = models.CharField(max_length=40)
    # Пол
    sex = models.CharField(max_length=10)
    # Номер взвода (ссылка на взвод)
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    # Должность во взводе
    military_post = models.CharField(max_length=255)
    # Логин в учетной системе
    login = models.CharField(max_length=30)
    # Пароль (в хэшированном виде)
    password = models.CharField(max_length=255)
    # Факультет в гражданском вузе
    department = models.CharField(max_length=255)
    # Номер группы на факультете
    group_number = models.IntegerField()
    # Статус студента (учится, выпустился или отчислен)
    active = models.CharField(max_length=30)

    class Meta:
        db_table = 'students'

    def json(self):
        return {'surname': self.surname, 
                    'name': self.name,
                    'patronymic': self.patronymic,
                    'sex': self.sex,
                    'platoon': self.platoon.json(),
                    'military_post': self.military_post,
                    'login': self.login,
                    'password': self.password,
                    'department': self.department,
                    'group_number': self.group_number,
                    'status': self.active
                    }

