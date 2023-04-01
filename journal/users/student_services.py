"""
Модуль бизнес-логики для сущности студента
"""
import logging, re
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField

from users.platoon_services import get_platoon_by_number
from .models import Student, Platoon
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)
_fio_regex = r'[А-Я]{1}[а-я]+'
_login_password_regex = r'^[a-z]+([-_]?[a-z0-9]+){0,2}$'
_posts = frozenset({'студент', 'командир взвода'})


def convert_students_to_json(students):
    """Переводит список студентов в виде QuerySet в JSON нотацию
    input:
        students -> список типа QuerySet
    output:
        students в виде json"""
    student_arr = list()
    for student in students:
        student_arr.append(student.json())
    return {'students': student_arr}


def validate_student_data(input_data):
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
        logger.error('student: surname field has invalid data for validation')
        raise ValidationError("Некорректное значение для фамилии")

    if re.fullmatch(_fio_regex, input_data['name']):
        result['name'] = input_data['name']
    else:
        logger.error('student: name field has invalid data for validation')
        raise ValidationError("Некорректное значение для имени")

    if re.fullmatch(_fio_regex, input_data['patronymic']):
        result['patronymic'] = input_data['patronymic']
    else:
        logger.error('student: patronymic field has invalid data for validation')
        raise ValidationError("Некорректное значение для отчества")

    if re.fullmatch(r'мужской|женский', input_data['sex']):
        result['sex'] = input_data['sex']
    else:
        logger.error('student: sex field has invalid data for validation')
        raise ValidationError("Выберите пол: мужской или женский")

    try:
        pl_number = get_platoon_by_number(input_data['platoon'])
        result['platoon'] = input_data['platoon']
    except Exception:
        logger.error('student: platoon field has invalid data for validation')
        raise ValidationError("Указан несуществующий номер взвода")

    if input_data['military_post'] in _posts:
        result['military_post'] = input_data['military_post']
    else:
        logger.error('student: military_post field has invalid data for validation')
        raise ValidationError("Некорректное значение для должности")

    if re.fullmatch(_login_password_regex, input_data['login']):
        result['login'] = input_data['login']
    else:
        logger.error('student: login field has invalid data for validation')
        raise ValidationError("Логин должен содержать только латинские буквы и цифры")

    if len(input_data['password']) < 8:
        logger.error('student: password field has incorrected length for validation')
        raise ValidationError("Пароль должен содержать не менее 8 символов")
    if re.fullmatch(_login_password_regex, input_data['password']):
        result['password'] = input_data['password']
    else:
        logger.error('student: password field has invalid data for validation')
        raise ValidationError("Пароль должен содержать только латинские буквы и цифры")

    if not input_data['department']:
        logger.error('student: department field has invalid data for validation')
        raise ValidationError("Пустое название факультета")
    else:
        result['department'] = input_data['department']

    if re.fullmatch(r'\d', input_data['group_number']):
        result['group_number'] = input_data['group_number']
    else:
        logger.error('student: group_number field has invalid data for validation')
        raise ValidationError("Некорректное значение для номера группы")

    return result


def get_student(student_id) -> Student:
    """Получить экземпляр студента по его номеру student_id
    input:
        student_id -> идентификатор студента в базе данных
    output:
        объект Student в случае успеха
        Exception в случае ошибки"""
    try:
        student = Student.objects.get(id=student_id)
        if student.studentprofile.active == 'отчислен':
            raise Exception("Студент с таким идентификатором отчислен!")
        return student
    except:
        logger.info(f'student with id {student_id} does not exist')
        raise Exception("Студента с таким идентификатором не существует!")


def add_new_student_to_db(validated_data):
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
    new_student = Student.objects.create_user(surname=validated_data['surname'], 
                          name=validated_data['name'], 
                          patronymic=validated_data['patronymic'],
                          military_post=validated_data['military_post'],
                          username=validated_data['login'],
                          password=validated_data['password'])
    
    new_student.studentprofile.sex = validated_data['sex']   
    new_student.studentprofile.platoon = get_platoon_by_number(validated_data['platoon'])
    new_student.studentprofile.department = validated_data['department']
    new_student.studentprofile.group_number = validated_data['group_number']
    new_student.studentprofile.active = 'учится'
    new_student.studentprofile.save()
    logger.info("create new student in database")


def update_existing_student(validated_data, id):
    """Обновить данные data о студенте с номером id
     input:
        validated_data -> dict с данными студента после валидации:
            - surname -> str с фамилией
            - name -> str с именем
            - patronymic -> str с отчеством
            - sex -> str с полом студента
            - platoon -> номер взвода (pk модели Platoon)
            - military_post -> str с должностью студента во взводе
            - password -> str с паролем пользователя
            - department -> str с факультетом студента в гражданском вузе
            - group_number -> str с номером группы студента в гражданском вузе
        id -> идентификатор студента в базе данных
    output:
        Exception -> в случае ошибки поиска студента"""
    student = getStudent(id)
    student.surname = validated_data['surname']
    student.name = validated_data['name']
    student.patronymic = validated_data['patronymic']
    student.studentprofile.sex = validated_data['sex']
    student.studentprofile.platoon = get_platoon_by_number(validated_data['platoon'])
    student.military_post = validated_data['military_post']
    student.password = CharField(make_password(validated_data['password']))
    student.studentprofile.department = validated_data['department']
    student.studentprofile.group_number = validated_data['group_number']
    student.studentprofile.save();
    student.save()
    logger.info("update existing student with id {id} in database")


def delete_student(id):
    """ Программно удалить студента с номером id из базы (отчислить с кафедры)
    input:
        id -> идентификатор студента в базе данных
    output:
        Exception -> в случае ошибки поиска студента"""
    student = getStudent(id)
    student.studentprofile.active = 'отчислен'
    student.studentprofile.save()
    logger.info("remove existing student with id {id} in database")









