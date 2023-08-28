"""
Модуль бизнес-логики для сущности студента
"""
from users.services.platoon import get_students_by_platoon
from users.serializers import StudentCreateSerializer

from users.models import StudentProfile


def get_student(student_id: int) -> StudentProfile:
    try:
        student = StudentProfile.objects.get(id=student_id)
        return student
    except:
        raise ValueError("Студента с таким идентификатором не существует!")


def add_new_student_to_db(student_data: dict) -> StudentProfile:
    if student_data['military_post'] == 'командир взвода' and \
            get_students_by_platoon(student_data['platoon']).get(military_post='командир взвода') != None:
                raise Exception('Командир взвода в данном взводе уже существует')
    serializer = StudentCreateSerializer(data=student_data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()
    

def update_existing_student(student_data: dict, student_id: int) -> StudentProfile:
    student = get_student(student_id)
    serializer = StudentCreateSerializer(student, data=student_data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def expulse_student(student_id) -> None:
    student = get_student(student_id)
    student.status = 'отчислен'
    student.save()
