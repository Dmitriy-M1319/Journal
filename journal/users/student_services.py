"""
Модуль бизнес-логики для сущности студента
"""
import logging, re
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField

from users.platoon_services import getPlatoonByNumber
from .models import Student, Platoon
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)
_fio_regex = r'[А-Я]{1}[а-я]+'
_login_password_regex = r'^[a-z]+([-_]?[a-z0-9]+){0,2}$'
_posts = frozenset({'студент', 'командир взвода'})


def validateStudentData(input_data):
    """Проверяет данные для студента в списке input_data на корректность
    input:
        input_data -> dict с проверяемыми следующими данными:
            - surname -> str с фамилией
            - name -> str с именем
            - patronymic -> str с отчеством
            - sex -> str с полом студента
            - platoon -> номер взвода (pk модели Platoon)
            - military_post -> str с должностью студента во взводе
            - login -> str с логином студента
            - password -> str с паролем пользователя
            - department -> str с факультетом студента в гражданском вузе
            - group_number -> str с номером группы студента в гражданском вузе
        output:
            dict, аналогичный входным данным, в случае успеха
            ValidationError -> в случае некорректных данных""" 
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

    try:
        pl_number = getPlatoonByNumber(input_data['platoon'])
        result['platoon'] = input_data['platoon']
    except Exception:
       raise ValidationError("Указан несуществующий номер взвода")

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
    input:
        student_id -> идентификатор студента в базе данных
    output:
        объект Student в случае успеха
        Exception в случае ошибки"""
    try:
        student = Student.objects.get(id=student_id)
        if student.active == 'отчислен':
            raise Exception("Студент с таким идентификатором отчислен!")
        return student
    except:
        raise Exception("Студента с таким идентификатором не существует!")


def _insertNewDataToStudentModel(new_student, data, active):
    """Заполнить экземпляр студента новыми данными"""
    new_student.surname = data['surname']
    new_student.name = data['name']
    new_student.patronymic = data['patronymic']
    new_student.sex = data['sex']
    new_student.platoon = getPlatoonByNumber(data['platoon'])
    new_student.military_post = data['military_post']
    new_student.login = data['login']
    new_student.password = CharField(make_password(data['password']))
    new_student.department = data['department']
    new_student.group_number = data['group_number']
    new_student.active = CharField(active)
    return new_student


def addNewStudent(validated_data):
    """Добавить нового студента с данными validated_data в базу
    input:
        validated_data -> dict с данными студента после валидации:
            - surname -> str с фамилией
            - name -> str с именем
            - patronymic -> str с отчеством
            - sex -> str с полом студента
            - platoon -> номер взвода (pk модели Platoon)
            - military_post -> str с должностью студента во взводе
            - login -> str с логином студента
            - password -> str с паролем пользователя
            - department -> str с факультетом студента в гражданском вузе
            - group_number -> str с номером группы студента в гражданском вузе"""
    new_student = _insertNewDataToStudentModel(Student(), validated_data, 'учится')
    new_student.save()
    logger.info("New student was created successfully")


def updateStudentInDb(validated_data, id):
    """Обновить данные data о студенте с номером id
     input:
        validated_data -> dict с данными студента после валидации:
            - surname -> str с фамилией
            - name -> str с именем
            - patronymic -> str с отчеством
            - sex -> str с полом студента
            - platoon -> номер взвода (pk модели Platoon)
            - military_post -> str с должностью студента во взводе
            - login -> str с логином студента
            - password -> str с паролем пользователя
            - department -> str с факультетом студента в гражданском вузе
            - group_number -> str с номером группы студента в гражданском вузе
        id -> идентификатор студента в базе данных
    output:
        Exception -> в случае ошибки поиска студента"""
    student = getStudent(id)
    student = _insertNewDataToStudentModel(student, validated_data, student.active)
    student.save()
    logger.info("Student was updated successfully")


def deleteStudentFromDb(id):
    """ Программно удалить студента с номером id из базы (отчислить с кафедры)
    input:
        id -> идентификатор студента в базе данных
    output:
        Exception -> в случае ошибки поиска студента"""
    student = getStudent(id)
    student.active = 'отчислен'
    student.save()
    logger.info("Student was removed successfully")









