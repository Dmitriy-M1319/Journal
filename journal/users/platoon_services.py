"""
Модуль бизнес-логики для взвода
"""
import logging

from users.models import Platoon, StudentProfile


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


def get_students_by_platoon(platoon_number):
    """ Получить список студентов взвода с номером platoon_number """
    platoon = get_platoon_by_number(platoon_number)
    students = StudentProfile.objects.filter(platoon=platoon)
    students = students.filter(active='study')
    return students


def delete_platoon(platoon_number):
    """ Выпустить взвод (удалить его программно) 
    input:
        platoon_number -> номер выпускаемого взвода"""
    platoon = get_platoon_by_number(platoon_number)
    platoon.status = 'выпустился'
    platoon.save()
    logger.info(f'delete platoon with number {platoon_number}')

