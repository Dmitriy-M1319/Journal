"""
Модуль бизнес-логики для сущности преподавателя
"""
from functools import cmp_to_key

from users.serializers import TeacherCreateSerializer
from users.models import TeacherProfile


_military_ranks = {
    'лейтенант': 0,
    'старший лейтенант': 1,
    'капитан': 2,
    'майор': 3, 
    'подполковник': 4, 
    'полковник': 5
}


def get_teacher(teacher_id: int) -> TeacherProfile:
    try:
          return TeacherProfile.objects.get(pk=teacher_id)
    except Exception:
        raise ValueError("Такого преподавателя не существует в базе")


def _compare_teachers(t1: TeacherProfile,  t2: TeacherProfile):
    if _military_ranks[str(t1.military_rank)] > _military_ranks[str(t2.military_rank)]:
        return 1 
    elif _military_ranks[str(t1.military_rank)] < _military_ranks[str(t2.military_rank)]:
        return -1
    else:
        return 0


def get_teachers_sorted_by_ranks():
    teachers = TeacherProfile.objects.all()
    return sorted(teachers, key=cmp_to_key(_compare_teachers))
    

def add_new_teacher_to_db(teacher_data) -> TeacherProfile:
    teacher_data.is_valid(raise_exception=True)
    return teacher_data.save()
     

def update_existing_teacher(data: dict, teacher_id) -> TeacherProfile:
    teacher = get_teacher(teacher_id)
    serializer = TeacherCreateSerializer(teacher, data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def dismiss_teacher(teacher_id):
    teacher = get_teacher(teacher_id)
    teacher.status = 'уволен'
    teacher.save()
