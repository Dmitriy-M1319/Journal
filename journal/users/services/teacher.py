"""
Модуль бизнес-логики для сущности преподавателя
"""
from functools import cmp_to_key
from typing import Dict, List
from users.models import User, TeacherProfile


# Перечень воинских званий на военной кафедре
_military_ranks = {
    'лейтенант': 0,
    'старший лейтенант': 1,
    'капитан': 2,
    'майор': 3, 
    'подполковник': 4, 
    'полковник': 5
}

# На будущее
_military_posts = {
    'преподаватель': 0,
    'старший преподаватель': 1,
    'начальник цикла - старший преподаватель': 2,
    'заместитель начальника кафедры': 3,
    'начальник кафедры': 4
}


def get_teacher(teacher_id: int) -> TeacherProfile:
    """
    Получить экземпляр преподавателя по его id
    """
    try:
        teacher = TeacherProfile.objects.get(pk=teacher_id)
        return teacher
    except Exception:
        raise Exception("Такого преподавателя не существует в базе")


def _compare_teachers(t1: TeacherProfile,  t2: TeacherProfile):
    """
    Компаратор для сравнения преподавателей
    """
    if _military_ranks[str(t1.military_rank)] > _military_ranks[str(t2.military_rank)]:
        return 1 
    elif _military_ranks[str(t1.military_rank)] < _military_ranks[str(t2.military_rank)]:
        return -1
    else:
        return 0


def get_sorted_teachers():
    """
    Получить преподавателей, отсортированных по воинским званиям и должностям
    """
    teachers = TeacherProfile.objects.all()
    return sorted(teachers, key=cmp_to_key(_compare_teachers))
    

def add_new_teacher_to_db(user: User, validated_data: dict) -> TeacherProfile:
    """
    Добавить нового преподавателя с данными из validated_data в базу
    """
    profile = TeacherProfile()
    profile.user = user
    profile.surname = validated_data['surname']
    profile.name = validated_data['name']
    profile.patronymic = validated_data['patronymic']
    profile.military_post = validated_data['military_post']
    profile.military_rank = validated_data['military_rank'] 
    profile.teacher_role = validated_data['teacher_role'] 
    profile.cycle = validated_data['cycle'] 
    profile.status = 'работает' 
    profile.save()
    return profile
     

def update_existing_teacher(user: User, validated_data: dict, teacher_id) -> TeacherProfile:
    """
    Обновить запись преподавателя с номером teacher_id данными validated_data
    """
    user.save()
    profile = get_teacher(teacher_id)
    profile.user = user
    profile.surname = validated_data['surname']
    profile.name = validated_data['name']
    profile.patronymic = validated_data['patronymic']
    profile.military_post = validated_data['military_post']
    profile.military_rank = validated_data['military_rank'] 
    profile.teacher_role = validated_data['teacher_role'] 
    profile.cycle = validated_data['cycle'] 
    profile.status = 'работает' 
    profile.save()
    return profile


def dismiss_teacher(teacher_id):
    """ 
    Уволить преподавателя
    """
    teacher = get_teacher(teacher_id)
    teacher.status = 'уволен'
    teacher.save()
