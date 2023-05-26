"""
Модуль бизнес-логики для сущности студента
"""
from django.contrib.auth.models import User

from users.services.platoon import get_platoon_by_number
from users.models import StudentProfile


def get_student(student_id: int) -> StudentProfile:
    """
    Получить экземпляр студента по его номеру student_id
    """
    try:
        student = StudentProfile.objects.get(id=student_id)
        return student
    except:
        raise Exception("Студента с таким идентификатором не существует!")


def add_new_student_to_db(user: User, validated_data: dict) -> StudentProfile:
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
    return profile


def update_existing_student(user: User, validated_data: dict, student_id) -> StudentProfile:
    """
    Обновить данные data о студенте с номером id
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
    return student


def expulse_student(id):
    """ 
    Отчислить студента
    """
    student = get_student(id)
    student.status = 'expulsed'
    student.save()
