"""
Модуль бизнес-логики для веб-сервисов преподавателя
"""
import logging

from .models import User, TeacherProfile


logger = logging.getLogger(__name__)


def get_teacher(teacher_id) -> TeacherProfile:
    """Получить экземпляр преподавателя по его id"""
    try:
        teacher = TeacherProfile.objects.get(pk=teacher_id)
        if teacher.status == 'уволен':
            raise Exception("В данный момент этот преподаватель не работает в учебном центре")
        return teacher
    except Exception:
        raise Exception("Такого преподавателя не существует в базе")


def add_new_teacher_to_db(user: User, validated_data):
    """Добавить нового преподавателя с данными из validated_data в базу
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
    logger.info('create new teacher in database')
    return profile
     

def update_existing_teacher(user: User, validated_data, teacher_id):
    """Обновить запись преподавателя с номером teacher_id данными validated_data
    """
    user.first_name = validated_data['first_name']
    user.last_name = validated_data['last_name']
    user.save()
    profile = get_teacher(teacher_id)
    profile.user = user
    profile.patronymic = validated_data['patronymic']
    profile.military_post = validated_data['military_post']
    profile.military_rank = validated_data['military_rank'] 
    profile.teacher_role = validated_data['role'] 
    profile.cycle = validated_data['cycle'] 
    profile.status = 'работает' 
    profile.save()
    logger.info(f'update existing teacher with id {teacher_id} in database')
    return profile


def delete_teacher(teacher_id):
    """ 'Уволить' (программно удалить) преподавателя из базы
    input:
        teacher_id -> идентификатор преподавателя в базе данных
    output:
        Exception -> в случае ошибки"""
    teacher = get_teacher(teacher_id)
    teacher.status = 'уволен'
    teacher.save()
    logger.info(f'remove existing teacher with id {teacher_id} in database')

