"""
Модуль бизнес-логики для веб-сервисов преподавателя
"""

import re
from .models import Teacher
from django.core.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.db.models.fields import CharField

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

    if re.fullmatch(_fio_regex, input_data['surname']):
        result['surname'] = input_data['surname']
    else:
       raise ValidationError("Некорректное значение для фамилии")

    if re.fullmatch(_fio_regex, input_data['name']):
        result['name'] = input_data['name']
    else:
       raise ValidationError("Некорректное значение для имени")

    if re.fullmatch(_fio_regex, input_data['patronymic']):
        result['patronymic'] = input_data['patronymic']
    else:
       raise ValidationError("Некорректное значение для отчества")

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

    if not input_data['cycle'] or input_data['cycle'] == '':
        raise ValidationError("Некорректное значение для воинской должности")
    else:
        result['cycle'] = input_data['cycle']

    if not input_data['role'] or input_data['role'] == '':
        raise ValidationError("Некорректное значение для роли в системе")
    else:
        result['role'] = input_data['role']

    if re.fullmatch(_login_password_regex, input_data['login']):
        result['login'] = input_data['login']
    else:
        raise ValidationError("Логин должен содержать только латинские буквы и цифры")

    if len(input_data['password']) < 8:
        raise ValidationError("Пароль должен содержать не менее 8 символов")
    if re.fullmatch(_login_password_regex, input_data['password']):
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
    teacher.role = data['role']
    teacher.cycle = data['cycle']
    teacher.login = data['login']
    teacher.password = CharField(make_password(data['password']))
    return teacher


def getTeacher(teacher_id) -> Teacher:
    """ Получить экземпляр преподавателя по его id
        В случае ошибки выбрасывается исключение Exception """
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
    teacher = getTeacher(teacher_id)
    teacher = _insertNewDataToTeacherModel(teacher, validated_data)
    teacher.save()


def deleteTeacherFromDatabase(teacher_id):
    """ 'Уволить' (программно удалить) преподавателя из базы """
    teacher = getTeacher(teacher_id)
    teacher.status = False
    teacher.save()

