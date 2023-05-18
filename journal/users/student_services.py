"""
Модуль бизнес-логики для сущности студента
"""
import logging
from django.contrib.auth.models import User

from users.platoon_services import get_platoon_by_number
from .models import StudentProfile

logger = logging.getLogger(__name__)


def get_student(student_id) -> StudentProfile:
    """Получить экземпляр студента по его номеру student_id
    input:
        student_id -> идентификатор студента в базе данных
    output:
        объект Student в случае успеха
        Exception в случае ошибки"""
    try:
        student = StudentProfile.objects.get(id=student_id)
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
                             group_number=validated_data['group_number'],
                             public_load=validated_data['public_load'],
                             order_of_expulsion=validated_data['order_of_expulsion'],
                             marital_status=validated_data['marital_status'],
                             address=validated_data['address'],
                             phone_number=validated_data['phone_number'],
                             sports_category=validated_data['sports_category'])

    profile.active = 'study'
    profile.save()
    logger.info("create new student in database")
    return profile


def update_existing_student(user: User, validated_data, student_id):
    """Обновить данные data о студенте с номером id
    """
    user.save()
    student = get_student(student_id)
    student.surname = validated_data['surname']
    student.name = validated_data['name']
    student.patronymic = validated_data['patronymic']
    student.platoon = get_platoon_by_number(validated_data['platoon'])
    student.military_post = validated_data['military_post']
    student.department = validated_data['department']
    student.group_number = validated_data['group_number']
    student.public_load = validated_data['public_load']
    student.order_of_expulsion = validated_data['order_of_expulsion']
    student.marital_status = validated_data['marital_status']
    student.address = validated_data['address']
    student.phone_number = validated_data['phone_number']
    student.sports_category = validated_data['sports_category']
    student.save();
    logger.info("update existing student with id {id} in database")
    return student


def delete_student(id):
    """ Удалить запись студента
    input:
        id -> идентификатор студента в базе данных
    output:
        Exception -> в случае ошибки поиска студента"""
    student = get_student(id)
    student.delete()
    student.save()
    logger.info("remove existing student with id {id} in database")









