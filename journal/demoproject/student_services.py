"""
Модуль бизнес-логики для сущности студента
"""
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField
from .models import Student, Platoon
from django.contrib.auth.hashers import make_password
import logging, re

logger = logging.getLogger(__name__)

# За такое меня надо захуярить сразу :)
def validateData(input_data):
    # прочитать про регулярные выражения и сделать проверки
    result = {}

    # Проверка фамилии на корректность
    match = re.fullmatch(r'[А-Я]{1}[а-я]+', input_data['surname'])
    if match:
        result['surname'] = input_data['surname']
    else:
       raise ValidationError("Некорректное значение для фамилии")

    # Проверка имени на корректность
    match = re.fullmatch(r'[А-Я]{1}[а-я]+', input_data['name'])
    if match:
        result['name'] = input_data['name']
    else:
       raise ValidationError("Некорректное значение для имени")

    # Проверка отчества на корректность
    match = re.fullmatch(r'[А-Я]{1}[а-я]+', input_data['patronymic'])
    if match:
        result['patronymic'] = input_data['patronymic']
    else:
       raise ValidationError("Некорректное значение для отчества")

    # Проверка пола на корректность
    match = re.fullmatch(r'мужской|женский', input_data['sex'])
    if match:
        result['sex'] = input_data['sex']
    else:
        raise ValidationError("Выберите пол: мужской или женский")

    # Проверка номера взвода на корректность
    pl_number = Platoon.objects.get(platoon_number=input_data['platoon']).first()
    if not pl_number:
       raise ValidationError("Указан несуществующий номер взвода")
    else:
        result['platoon'] = input_data['platoon']

    # Проверка должности на корректность
    match = re.fullmatch(r'студент|командир взвода', input_data['military_post'])
    if match:
        result['military_post'] = input_data['military_post']
    else:
        raise ValidationError("Некорректное значение для должности")

    # Проверка логина на корректность
    match = re.fullmatch(r'^[a-z]+([-_]?[a-z0-9]+){0,2}$', input_data['login'])
    if match:
        result['login'] = input_data['login']
    else:
        raise ValidationError("Логин должен содержать только латинские буквы и цифры")

    # Проверка пароля на корректность
    if len(input_data['password']) < 8:
        raise ValidationError("Пароль должен содержать не менее 8 символов")

    match = re.fullmatch(r'^[a-z]+([-_]?[a-z0-9]+){0,2}$', input_data['password'])
    if match:
        result['password'] = input_data['password']
    else:
        raise ValidationError("Пароль должен содержать только латинские буквы и цифры")

    # Проверка факультета на корректность
    if not input_data['department']:
        raise ValidationError("Пустое название факультета")
    else:
        result['department'] = input_data['department']

    # Проверка номера группы на корректность
    match = re.fullmatch(r'\d', input_data['group_number'])
    if match:
        result['group_number'] = input_data['group_number']
    else:
        raise ValidationError("Некорректное значение для номера группы")

    return result

def createNewStudent(new_student, data, active):
    new_student = Student()
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

def addStudent(data):
    new_student = Student()
    createNewStudent(new_student, data, 'учится')    
    new_student.save()
    logger.info("New student was created successfully")


def updateStudentInDb(data, id):
    """Обновить данные о студенте с номером id"""
    student = Student.objects.get(id=id).first()
    if not student:
        raise Exception("Студента с таким идентификатором не существует!")
   
    result_data = validateData(data)
    if student.active == 'отчислен':
        raise Exception("Студент с таким идентификатором отчислен!")

    createNewStudent(student, data, student.active)
    student.save()
    logger.info("Student was updated successfully")

def deleteStudentFromDb(id):
    student = Student.objects.get(id=id).first()
    if not student:
        raise Exception("Студента с таким идентификатором не существует!")
   
    if student.active == 'отчислен':
        raise Exception("Студент с таким идентификатором отчислен!")

    student.active = 'отчислен'
    student.save()
    logger.info("Student was removed successfully")









