"""
    Модели пользователей в веб-приложении электронного журнала
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.fields import proxy


class CustomUser(AbstractUser):
    """Модель с общими данными для студента и преподавателя для авторизации"""
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
    # Фамилия
    surname = models.CharField(max_length=40)
    # Имя
    name = models.CharField(max_length=40)
    # Отчество
    patronymic = models.CharField(max_length=40)
    # Воинская должность
    military_post = models.CharField(max_length=255)
    base_role = Role.ADMIN
    role = models.CharField(null=True, max_length=50, choices=Role.choices)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.STUDENT)


class Student(CustomUser):
    """Модель студента для авторизации"""
    base_role = CustomUser.Role.STUDENT
    student = StudentManager()
    class Meta:
        proxy = True


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.TEACHER)


class Teacher(CustomUser):
    """Модель преподавателя на кафедре для авторизации"""
    base_role = CustomUser.Role.TEACHER
    teacher = TeacherManager()
    class Meta:
        proxy = True


class TeacherProfile(models.Model):
    """Модель профиля преподавателя на кафедре"""
    user = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    # Воинское звание
    military_rank = models.CharField(max_length=20)
    # Цикл
    cycle = models.CharField(max_length=255)
    # Роль в системе (обычный преподаватель или суперпользователь)
    teacher_role = models.IntegerField()
    # Статус преподавателя (работает или уволен)
    status = models.CharField(max_length=30)

    def json(self):
        return {'surname': self.user.surname, 
                    'name': self.user.name,
                    'patronymic': self.user.patronymic,
                    'military_rank': self.military_rank,
                    'military_post': self.user.military_post,
                    'cycle': self.cycle,
                    'login': self.user.username,
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


class StudentProfile(models.Model):
    """Модель профиля студента на кафедре"""
    user = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    # Пол
    sex = models.CharField(max_length=10)
    # Номер взвода (ссылка на взвод)
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    # Факультет в гражданском вузе
    department = models.CharField(max_length=255)
    # Номер группы на факультете
    group_number = models.IntegerField()
    # Статус студента (учится, выпустился или отчислен)
    active = models.CharField(max_length=30)

    def json(self):
        return {'surname': self.user.surname, 
                    'name': self.user.name,
                    'patronymic': self.user.patronymic,
                    'sex': self.sex,
                    'platoon': self.platoon.json(),
                    'military_post': self.user.military_post,
                    'login': self.user.login,
                    'department': self.department,
                    'group_number': self.group_number,
                    'status': self.active
                    }

