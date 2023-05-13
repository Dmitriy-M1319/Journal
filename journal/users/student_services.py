"""
Модуль бизнес-логики для сущности студента
"""
import logging, re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField

from users.platoon_services import get_platoon_by_number
from .models import StudentProfile

logger = logging.getLogger(__name__)
_fio_regex = r'[А-Я]{1}[а-я]+'
_login_password_regex = r'^[a-z]+([-_]?[a-z0-9]+){0,2}$'
_posts = {'студент', 'командир взвода'}


def get_student(student_id) -> StudentProfile:
    """Получить экземпляр студента по его номеру student_id
    input:
        student_id -> идентификатор студента в базе данных
    output:
        объект Student в случае успеха
        Exception в случае ошибки"""
    try:
        student = StudentProfile.objects.get(id=student_id)
        if student.active == 'отчислен':
            raise Exception("Студент с таким идентификатором отчислен!")
        return student
    except:
        logger.info(f'student with id {student_id} does not exist')
        raise Exception("Студента с таким идентификатором не существует!")


def add_new_student_to_db(user: User, validated_data):
    """Добавить нового студента"""
    platoon = get_platoon_by_number(validated_data['platoon'])
    profile = StudentProfile(user=user,
                             surname=validated_data['surname'],
                             name=validated_data['name'],
                             patronymic=validated_data['patronymic'],
                             military_post=validated_data['military_post'],
                             platoon=platoon,
                             department=validated_data['department'],
                             group_number=validated_data['group_number'])

    profile.active = 'учится'
    profile.save()
    logger.info("create new student in database")
    return profile


def update_existing_student(user: User, validated_data, student_id):
    """Обновить данные data о студенте с номером id
    """
    student = get_student(student_id)
    user.last_name = validated_data['last_name']
    user.first_name = validated_data['first_name']
    student.patronymic = validated_data['patronymic']
    student.platoon = get_platoon_by_number(validated_data['platoon'])
    student.military_post = validated_data['military_post']
    student.department = validated_data['department']
    student.group_number = validated_data['group_number']
    student.save();
    logger.info("update existing student with id {id} in database")
    return student


def delete_student(id):
    """ Программно удалить студента с номером id из базы (отчислить с кафедры)
    input:
        id -> идентификатор студента в базе данных
    output:
        Exception -> в случае ошибки поиска студента"""
    student = get_student(id)
    student.active = 'отчислен'
    student.save()
    logger.info("remove existing student with id {id} in database")









