"""
Модуль, предоставляющий сервисы для работы с расписанием и занятиями
"""
# TODO: Посидеть над логгированием
from datetime import date, datetime

from django.core.exceptions import ValidationError
from users.models import Platoon, Teacher
from django.http import HttpRequest
from .models import SubjectClass, Subject

import re

""" Регулярное выражение для проверки даты и времени из запроса"""
_datetime_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'

""" Регулярное выражение для проверки даты из запроса"""
_date_pattern = r'\d{4}-\d{2}-\d{2}'

def getPlatoonTimetable(platoon: Platoon, day: date) -> dict:
    """Составить расписание для взвода platoon на определенный день day"""
    classes = platoon.subject_class_set().filter(class_date__date==day).order_by('date')
    if not classes:
        raise Exception("У данного взвода нет занятий в этот день")
    else:
        return classes.values()
        

def getDateFromStr(local_date:str):
    """Получить объект date из запроса HttpRequest"""
    if not re.fullmatch(_date_pattern, local_date):
        raise Exception("Некорректные данные для даты")
    else:
        date_lst = local_date.split('-')
        return date(int(date_lst[0]), int(date_lst[1]), int(date_lst[2]))


def getSubject(subject_id) -> Subject:
    """ Получить экземпляр предмета по его id
        В случае ошибки выбрасывается исключение Exception """
    subject = Subject.objects.get(id=subject_id)
    if not subject:
        raise Exception("Такого предмета не существует в базе")
    else:
        return subject


def validateSubjectData(input_data):
    """Проверяет данные для добавления нового предмета на корректность
        В случае ошибки выбрасывает Validation Error"""
    result = dict()
    teacher = Teacher.objects.get(id=input_data["teacher"])
    if not teacher:
        raise ValidationError("Некорректно указан преподаватель")
    else:
        result["teacher"] = input_data["teacher"]
    
    if not input_data["name"] or input_data["name"] == '':
        raise ValidationError("Некорректные данные для названия предмета")
    else:
        result["name"] = input_data["name"]

    if input_data["hours"].isnumeric() and int(input_data["hours"]) > 0:
        result["hours"] = input_data["hours"]
    else:
        raise ValidationError("Некорректные данные для количества часов")

    # TODO: Уточнить главные формы предметов, только экзамен или зачет или еще какие-то есть
    if not input_data["form"] or input_data["form"] == '':
        raise ValidationError("Некорректные данные для формы")
    else:
        result["form"] = input_data["form"]
    return result


def _insertNewDataToSubject(new_subject, data):
    """Заполнить экземпляр студента новыми данными"""
    new_subject["teacher"] = data["teacher"]
    new_subject["name"] = data["name"]
    new_subject["hours"] = data["hours"]
    new_subject["form"] = data["form"]
    return new_subject;


def addSubjectToDb(validated_data):
    """Добавить в базу данных новый предмет"""
    new_subject = _insertNewDataToSubject(Subject(), validated_data)
    new_subject.save()


def updateSubjectInDb(validated_data, id):
    """Обновить существующий предмет в базе данных"""
    subject = getSubject(id)
    subject = _insertNewDataToSubject(subject, validated_data)
    subject.save()


def deleteSubjectFromDb(id):
    """Удалить предмет из базы данных"""
    subject = getSubject(id)
    subject.delete()


def validateSubjectClassData(input_data: dict):
    """Проверить на корректность данные для занятия по предмету
        В случае ошибки выбрасывает ValidationError"""
    result = {}
    subject = Subject.objects.get(id=input_data["subject"])
    if not subject:
        raise ValidationError("Такого предмета не существует")
    else:
        result["subject"] = input_data["subject"]

    pl_number = Platoon.objects.get(platoon_number=input_data['platoon'])
    if not pl_number:
       raise ValidationError("Указан несуществующий номер взвода")
    else:
        result['platoon'] = input_data['platoon']

    if re.fullmatch(_datetime_pattern, input_data['class_date']):
        result["class_date"] = input_data["class_date"]
    else:
        raise ValidationError("Некорректные данные для даты и времени занятия")

    if input_data["theme_number"].isnumeric() and int(input_data["theme_number"]) > 0:
        result["theme_number"] = input_data["theme_number"]
    else:
        raise ValidationError("Некорректные данные для номера темы")

    if not input_data["theme_name"] or input_data["theme_name"] == '':
        raise ValidationError("Некорректные данные для названия темы")
    else:
        result["theme_name"] = input_data["theme_name"]

    if input_data["class_number"].isnumeric() and int(input_data["class_number"]) > 0:
        result["class_number"] = input_data["class_number"]
    else:
        raise ValidationError("Некорректные данные для номера занятия")

    if not input_data["class_name"] or input_data["class_name"] == '':
        raise ValidationError("Некорректные данные для названия занятия")
    else:
        result["class_name"] = input_data["class_name"]
    
    if not input_data["class_type"] or input_data["class_type"] == '':
        raise ValidationError("Некорректные данные для типа занятия")
    else:
        result["class_type"] = input_data["class_type"]

    if input_data["classroom"].isnumeric() and int(input_data["classroom"]) > 0:
        result["classroom"] = input_data["classroom"]
    else:
        raise ValidationError("Некорректные данные для номера аудитории")
    return result


def getSubjectClass(id):
    """ Получить экземпляр занятия по его id
        В случае ошибки выбрасывается исключение Exception """
    subject_class = SubjectClass.objects.get(id=id)
    if not subject_class:
        raise Exception("Такого занятия не существует в базе")
    else:
        return subject_class


def getDateAndTimeFromStr(date_time:str):
    """ Преобразовать дату и время в виде строки в объект datetime """
    local_datetime = date_time.split('T')
    local_date = getDateFromStr(local_datetime[0])
    time_lst = local_datetime[1].split(':')
    return datetime(local_date.year, local_date.month, local_date.day, int(time_lst[0]), int(time_lst[1]))

def _insertNewDataToSubjectClass(new_class, data):
    """ Внести новые данные в экземпляр занятия """
    new_class.platoon = data["platoon"]
    new_class.subject = data["subject"]
    new_class.class_date = getDateAndTimeFromStr(data["class_date"])
    new_class.theme_numbe = data["theme_number"]
    new_class.theme_name = data["theme_name"]
    new_class.class_number = data["class_number"]
    new_class.class_name = data["class_name"]
    new_class.class_type = data["class_type"]
    new_class.classroom = data["classroom"]
    return new_class


def addSubjectClassToDb(validated_data):
    """ Добавить в базу данных новое занятие """
    new_class = _insertNewDataToSubjectClass(SubjectClass(), validated_data)
    new_class.save()


def updateSubjectClassInDb(validated_data, id):
    """ Обновить в базе данных существующее занятие """
    subj_class = getSubjectClass(id)
    subj_class = _insertNewDataToSubjectClass(subj_class, validated_data)
    subj_class.save()


def deleteSubjectClassFromDb(id):
    """ Удалить занятие из базы данных """
    subj_class = getSubjectClass(id)
    subj_class.delete()
