"""
    Модуль бизнес-логики для взвода
"""

import re
import logging
from datetime import date

from users.teacher_services import getTeacher
from .models import Platoon, Teacher
from django.core.validators import ValidationError

logger = logging.getLogger(__name__)

def getPlatoonByNumber(platoon_number):
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


def getAllPlatoons():
    """ Получить все взводы на кафедре
    output:
        list: Platoon -> список объектов взвода"""
    return Platoon.objects.all().values()


def getStudentsByPlatoonFromDb(platoon_number):
    platoon = getPlatoonByNumber(platoon_number)
    return platoon.student_set.all()


def validateDataForPlatoon(input_data):
    """ Проверяет корректность входных данных для взвода
    input:
        input_data -> dict со следующими ключами:
            - platoon_number -> номер взвода
            - tutor -> id преподавателя-куратора
            - year -> год зачисления взвода на кафедру
            - status -> статус нахождения взвода на кафедре
    output:
        dict, аналогичный входным данным, в случае успеха
        ValidationError -> в случае некорректных данных"""
    result = dict()
    if not input_data['platoon_number'] or input_data['platoon_number'] == '' or not input_data['platoon_number'].isnumeric():
        logger.error('platoon_number field has invalid data for validation')
        raise ValidationError("Некорректные данные для номера взвода")
    else:
        result['platoon_number'] = input_data['platoon_number']

    try:
        tutor = getTeacher(input_data['tutor'])
        result['tutor'] = input_data['tutor']
    except:
        logger.error('tutor field has invalid data for validation')
        raise ValidationError("Такого преподавателя не существует")
 
    year = date.today().year
    if int(input_data['year']) > year:
        logger.error('year field has invalid data for validation')
        raise ValidationError('Некорректное значение для года набора')
    else:
        result['year'] = input_data['year']


    if re.fullmatch(r'учится|выпустился', input_data['status']):
        result['status'] = input_data['status']
    else:
        logger.error('status field has invalid data for validation')
        raise ValidationError('Некорректное значение для статуса взвода')

    return result


def _insertNewDataIntoPlatoonModel(platoon_model: Platoon, data, status):
    """ Занести в экземпляр взвода новые данные и статус """
    platoon_model.platoon_number = data['platoon_number']
    platoon_model.tutor = Teacher.objects.get(id=data['tutor'])
    platoon_model.year = int(data['year'])
    platoon_model.status = status
    return platoon_model


def addNewPlatoon(validated_data: dict):
    """ Добавить новый взвод в базу 
    input:
        validated_data -> dict c выхода функции валидации данных взвода:
            - platoon_number -> номер взвода
            - tutor -> id преподавателя-куратора
            - year -> год зачисления взвода на кафедру
            - status -> статус нахождения взвода на кафедре"""
    platoon = _insertNewDataIntoPlatoonModel(Platoon(), validated_data, 'учится')
    platoon.save()
    logger.info('save new platoon to database')


def updateExistingPlatoon(validated_data, platoon_number):
    """ Обновить данные существующего взвода 
    input:
        validated_data -> dict c выхода функции валидации данных взвода:
            - platoon_number -> номер взвода
            - tutor -> id преподавателя-куратора
            - year -> год зачисления взвода на кафедру
            - status -> статус нахождения взвода на кафедре
        platoon_number -> номер обновляемого взвода"""
    platoon = getPlatoonByNumber(platoon_number)
    platoon = _insertNewDataIntoPlatoonModel(platoon, validated_data, platoon.status)
    platoon.save() 
    logger.info(f'update platoon with number {platoon_number} in database')


def deletePlatoonWithGraduation(platoon_number):
    """ Выпустить взвод (удалить его программно) 
    input:
        platoon_number -> номер выпускаемого взвода"""
    platoon = getPlatoonByNumber(platoon_number)
    platoon.status = 'выпустился'
    platoon.save()
    logger.info(f'delette platoon with number {platoon_number}')

