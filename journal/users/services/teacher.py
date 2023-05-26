"""
Модуль бизнес-логики для сущности преподавателя
"""
from users.models import User, TeacherProfile


def get_teacher(teacher_id: int) -> TeacherProfile:
    """
    Получить экземпляр преподавателя по его id
    """
    try:
        teacher = TeacherProfile.objects.get(pk=teacher_id)
        return teacher
    except Exception:
        raise Exception("Такого преподавателя не существует в базе")


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
