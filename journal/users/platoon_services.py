"""
    Модуль бизнес-логики для взвода
"""

import re
import logging
from datetime import date

from users.teacher_services import get_teacher
from .models import Platoon, TeacherProfile
from django.core.validators import ValidationError

logger = logging.getLogger(__name__)

def get_platoon_by_number(platoon_number):
    """ Получить взвод по номеру platoon_number
    input:
        platoon_number -> номер взвода
    output:
        объект Platoon
        Exception -> в случае ошибки"""
    try:
        platoon = Platoon.objects.get(platoon_number=platoon_number)
        return platoon
    except:
        logger.error(f'get platoon with platoon_number {platoon_number}: failed')
        raise Exception('Взвода с таким номером не существует в базе')


def _insert_new_data_into_platoon(platoon_model: Platoon, data, status):
    """ Занести в экземпляр взвода новые данные и статус """
    platoon_model.platoon_number = data['platoon_number']
    platoon_model.tutor = TeacherProfile.objects.get(id=data['tutor'])
    platoon_model.year = int(data['year'])
    platoon_model.status = status
    return platoon_model


def add_new_platoon_to_db(validated_data: dict):
    """ Добавить новый взвод в базу 
    input:
        validated_data -> dict c выхода функции валидации данных взвода:
            - platoon_number -> номер взвода
            - tutor -> id преподавателя-куратора
            - year -> год зачисления взвода на кафедру
            - status -> статус нахождения взвода на кафедре"""
    platoon = _insert_new_data_into_platoon(Platoon(), validated_data, 'учится')
    platoon.save()
    logger.info('save new platoon to database')


def update_existing_platoon(validated_data, platoon_number):
    """ Обновить данные существующего взвода 
    input:
        validated_data -> dict c выхода функции валидации данных взвода:
            - platoon_number -> номер взвода
            - tutor -> id преподавателя-куратора
            - year -> год зачисления взвода на кафедру
            - status -> статус нахождения взвода на кафедре
        platoon_number -> номер обновляемого взвода"""
    platoon = get_platoon_by_number(platoon_number)
    platoon = _insert_new_data_into_platoon(platoon, validated_data, platoon.status)
    platoon.save() 
    logger.info(f'update platoon with number {platoon_number} in database')


def delete_platoon(platoon_number):
    """ Выпустить взвод (удалить его программно) 
    input:
        platoon_number -> номер выпускаемого взвода"""
    platoon = get_platoon_by_number(platoon_number)
    platoon.status = 'выпустился'
    platoon.save()
    logger.info(f'delette platoon with number {platoon_number}')

