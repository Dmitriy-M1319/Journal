"""
    Модуль бизнес-логики для взвода
"""

import re
from datetime import date

from django.db.models.fields import IntegerField

from users.teacher_services import getTeacher
from .models import Platoon, Teacher
from django.core.validators import ValidationError

def getPlatoonByNumber(platoon_number):
    """ Получить взвод по номеру platoon_number
        В случае неудачи выбрасывается Exception"""
    #TODO: Переписать обработку запроса в try/except
    platoon = Platoon.objects.get(platoon_number=platoon_number)
    if not platoon:
        raise Exception('Взвода с таким номером не существует в базе')
    else:
        return platoon


def validateDataForPlatoon(input_data):
    """ Проверяет входные данные для взвода
        В случае невалидности выбрасывает исключение ValidateError """
    result = dict()
    if not input_data['platoon_number'] or input_data['platoon_number'] == '' or not input_data['platoon_number'].isnumeric():
        raise ValidationError("Некорректные данные для номера взвода")
    else:
        result['platoon_number'] = input_data['platoon_number']

    try:
        tutor = getTeacher(input_data['tutor'])
        result['tutor'] = input_data['tutor']
    except:
        raise ValidationError("Такого преподавателя не существует")
 
    year = date.today().year
    if int(input_data['year']) > year:
        raise ValidationError('Некорректное значение для года набора')
    else:
        result['year'] = input_data['year']


    if re.fullmatch(r'учится|выпустился', input_data['status']):
        result['status'] = input_data['status']
    else:
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
    """ Добавить новый взвод в базу """
    platoon = _insertNewDataIntoPlatoonModel(Platoon(), validated_data, 'учится')
    platoon.save()


def updateExistingPlatoon(validated_data, platoon_number):
    """ Обновить данные существующего взвода """
    platoon = getPlatoonByNumber(platoon_number)
    platoon = _insertNewDataIntoPlatoonModel(platoon, validated_data, platoon.status)
    platoon.save() 


def deletePlatoonWithGraduation(platoon_number):
    """ Выпустить взвод (удалить его программно) """
    platoon = getPlatoonByNumber(platoon_number)
    platoon.status = 'выпустился'
    platoon.save()

