"""
Модуль бизнес-логики для сущности студента
"""
import logging, re
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField
from .models import Student, Platoon
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)
_fio_regex = r'[А-Я]{1}[а-я]+'
_login_password_regex = r'^[a-z]+([-_]?[a-z0-9]+){0,2}$'
_posts = frozenset({'студент', 'командир взвода'})


def validateStudentData(input_data):
    """Проверяет данные для студента в списке input_data на корректность""" 
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

    if re.fullmatch(r'мужской|женский', input_data['sex']):
        result['sex'] = input_data['sex']
    else:
        raise ValidationError("Выберите пол: мужской или женский")

    pl_number = Platoon.objects.get(platoon_number=input_data['platoon'])
    if not pl_number:
       raise ValidationError("Указан несуществующий номер взвода")
    else:
        result['platoon'] = input_data['platoon']

    if input_data['military_post'] in _posts:
        result['military_post'] = input_data['military_post']
    else:
        raise ValidationError("Некорректное значение для должности")

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

    if not input_data['department']:
        raise ValidationError("Пустое название факультета")
    else:
        result['department'] = input_data['department']

    if re.fullmatch(r'\d', input_data['group_number']):
        result['group_number'] = input_data['group_number']
    else:
        raise ValidationError("Некорректное значение для номера группы")

    return result


def getStudent(student_id) -> Student:
    """Получить экземпляр студента по его номеру student_id
        В случае ошибки выбрасывает исключение Exception"""
    student = Student.objects.get(id=id).first()
    if not student:
        raise Exception("Студента с таким идентификатором не существует!")
    elif student.active == 'отчислен':
        raise Exception("Студент с таким идентификатором отчислен!")
    else:
        return student


def _insertNewDataToStudentModel(new_student, data, active):
    """Заполнить экземпляр студента новыми данными"""
    new_student.surname = data['surname']
    new_student.name = data['name']
    new_student.patronymic = data['patronymic']
    new_student.sex = data['sex']
    new_student.platoon = data['platoon']
    new_student.military_post = data['military_post']
    new_student.login = data['military_post']
    new_student.password = CharField(make_password(data['password']))
    new_student.department = data['department']
    new_student.group_number = data['group_number']
    new_student.active = CharField(active)
    return new_student


def addNewStudent(validated_data):
    """Добавить нового студента с данными validated_data в базу"""
    new_student = _insertNewDataToStudentModel(Student(), validated_data, 'учится')
    new_student.save()
    logger.info("New student was created successfully")


def updateStudentInDb(validated_data, id):
    """Обновить данные data о студенте с номером id
        В случае ошибки выбрасывает исключение Exception"""
    student = getStudent(id)
    student = _insertNewDataToStudentModel(student, validated_data, student.active)
    student.save()
    logger.info("Student was updated successfully")

def deleteStudentFromDb(id):
    """ Программно удалить студента с номером id из базы (отчислить с кафедры)
        В случае ошибки выбрасывает исключение Exception"""
    student = getStudent(id)
    student.active = CharField('отчислен')
    student.save()
    logger.info("Student was removed successfully")









