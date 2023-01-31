"""
Модуль бизнес-логики для веб-сервисов преподавателя
"""

import re
from .models import Teacher
from django.core.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.db.models.fields import CharField, BooleanField

_fio_regex = r'[А-Я]{1}[а-я]+'
_login_password_regex = r'^[a-z]+([-_]?[a-z0-9]+){0,2}$'
_ranks = frozenset({'лейтенант',
          'старший лейтенант',
          'капитан',
          'майор',
          'подполковник',
          'полковник'})


def validateTeacherData(input_data):
    """Проверить входящие данные преподавателя на корректность"""
    result = {}

    # Проверка фамилии на корректность
    match = re.fullmatch(_fio_regex, input_data['surname'])
    if match:
        result['surname'] = input_data['surname']
    else:
       raise ValidationError("Некорректное значение для фамилии")

    # Проверка имени на корректность
    match = re.fullmatch(_fio_regex, input_data['name'])
    if match:
        result['name'] = input_data['name']
    else:
       raise ValidationError("Некорректное значение для имени")

    # Проверка отчества на корректность
    match = re.fullmatch(_fio_regex, input_data['patronymic'])
    if match:
        result['patronymic'] = input_data['patronymic']
    else:
       raise ValidationError("Некорректное значение для отчества")

    # Проверка воинского звания на корректность
    if input_data['military_rank'] in _ranks:
        result['military_rank'] = input_data['military_rank']
    else:
        raise ValidationError("Некорректное значение для воинского звания")
    
    # Проверка должности на корректность (TODO: узнать все должности на кафедре
    # Пока будет проверка на наличие
    if not input_data['military_post'] or input_data['military_post'] == '':
        raise ValidationError("Некорректное значение для воинской должности")
    else:
        result['military_post'] = input_data['military_post']

    # Проверка названия цикла
    if not input_data['cycle'] or input_data['cycle'] == '':
        raise ValidationError("Некорректное значение для воинской должности")
    else:
        result['military_post'] = input_data['military_post']

    # Проверка логина на корректность
    match = re.fullmatch(_login_password_regex, input_data['login'])
    if match:
        result['login'] = input_data['login']
    else:
        raise ValidationError("Логин должен содержать только латинские буквы и цифры")

    # Проверка пароля на корректность
    if len(input_data['password']) < 8:
        raise ValidationError("Пароль должен содержать не менее 8 символов")

    match = re.fullmatch(_login_password_regex, input_data['password'])
    if match:
        result['password'] = input_data['password']
    else:
        raise ValidationError("Пароль должен содержать только латинские буквы и цифры")

    return result


def _insertNewDataToTeacherModel(teacher, data):
    """Заполнить переданный экземпляр преподавателя teacher новыми данными из data"""
    teacher.name = data['name']
    teacher.surname = data['surname']
    teacher.patronymic = data['patronymic']
    teacher.military_rank = data['military_rank']
    teacher.military_post = data['military_post']
    teacher.cycle = data['cycle']
    teacher.login = data['login']
    teacher.password = CharField(make_password(data['password']))
    return teacher


def _getTeacher(teacher_id) -> Teacher:
    teacher = Teacher.objects.get(id=teacher_id)
    if not teacher:
        raise Exception("Такого преподавателя не существует в базе")
    else:
        return teacher

def addNewTeacherToDatabase(validated_data):
    """Добавить нового преподавателя с данными из validated_data в базу"""
    new_teacher = _insertNewDataToTeacherModel(Teacher(), validated_data)
    new_teacher.status = True
    new_teacher.save()
     

def updateExistingTeacher(validated_data, teacher_id):
    """Обновить запись преподавателя с номером teacher_id данными validated_data"""
    teacher = _getTeacher(teacher_id)
    teacher = _insertNewDataToTeacherModel(teacher, validated_data)
    teacher.save()


def deleteTeacherFromDatabase(teacher_id):
    """ 'Уволить' (программно удалить) преподавателя из базы """
    teacher = _getTeacher(teacher_id)
    teacher.status = False
    teacher.save()

