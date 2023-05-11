"""
Модуль бизнес-логики для работы с оценками в электронном журнале
"""

import re
from django.core.validators import ValidationError
from users.platoon_services import get_all_platoons, get_students_by_platoon
from marks.models import JournalCeil
from users.student_services import get_student
from timetable.timetable_service import getSubject, getSubjectClass, getSubjectClassesBySubject, get_classes_by_platoon_and_subject

_attendance_regex = r'был|неуваж.причина|болен|справка'
_mark_regex = r'[2-5]{1,1}'

def validateMarkData(input_data: dict):
    """Проверяет на корректность входные данные для ячейки журнала
    input:
        input_data -> dict, входные данные:
            - student -> id студента
            - subject_class -> id занятия
            - mark -> оценка в str типе
            - attendance -> посещаемость в str типе
    output:
        dict с выходными данными:
            - student - объект Student
            - subject_class - объект SubjectClass
            - mark - str с целым числом
            - attendance - str
        или ValidationError в случае ошибки"""
    result = {}
    try:
        existing_student = get_student(input_data['student'])
        result['student'] = existing_student

        subject_class = getSubjectClass(input_data['subject_class'])
        result['subject_class'] = subject_class
    except Exception as e:
        raise ValidationError(e)

    if re.fullmatch(_mark_regex, input_data['mark']):
        result['mark'] = input_data['mark']
    else:
        raise ValidationError('Значение оценки не корректно в данной образовательной системе')

    if re.fullmatch(_attendance_regex, input_data['attendance']):
        result['attendance'] = input_data['attendance']
    else:
        raise ValidationError('Значение посещаемости не является корректным')

    return result


def getJournalCeil(journal_id):
    """Получает объект ячейки по его id
    input:
        journal_id -> id ячейки
    output:
        JournalCeil -> объект ячейки
        Exception -> в случае ошибки"""
    try:
        ceil = JournalCeil.objects.get(id=journal_id)
        return ceil
    except:
        raise Exception('Такой ячейки не существует')


def get_all_journal_ceils_by_platoons():
    """Получить все оценки, распределяя их по студентам"""
    platoons = get_all_platoons()
    all_marks = dict()
    # Собираем список из студентов
    for platoon in platoons:
        all_marks[platoon] = get_students_by_platoon(platoon.platoon_number)


def get_ceils_by_platoon_and_subject(subject_id, platoon_number):
    """ Получить оценки взвода по определенному предмету """
    students = get_students_by_platoon(platoon_number)
    platoon_classes = get_classes_by_platoon_and_subject(platoon_number, subject_id)
    ceils = dict()
    for student in students:
        


def getJournalCeilsForStudent(student_id):
    """Получить список оценок для студента по student_id
    input:
        student_id -> id студента
    output:
        list с объектами JournalCeil -> список ячеек
        Exception -> в случае ошибки"""
    current_student = get_student(student_id)
    journal_ceils = JournalCeil.objects.filter(student=current_student).order_by('id')
    return journal_ceils.values()


def getJournalCeilsBySubject(subject_id):
    """Получить список оценок по определенному предмету с subject_id
    input:
        subject_id -> id предмета для выборки
    output:
        dict [SubjectClass] - [list(JournalCeil)] -> список ячеек
        Exception -> в случае ошибки"""
    result = dict()
    subject_classes = getSubjectClassesBySubject(subject_id) 
    for s_class in subject_classes:
        ceils = JournalCeil.objects.filter(subject_class=s_class).order_by('id')
        result[s_class] = ceils.values()
    return result

        
def _insertNewDataInJournalCeil(ceil_object, data):
    ceil_object.student = data['student']
    ceil_object.subject_class = data['subject_class']
    ceil_object.mark = data['mark']
    ceil_object.attendance = data['attendance']
    return ceil_object


def addNewJournalCeil(validated_data: dict):
    """Добавить в базу данных новую ячейку
    input:
        validated_data - dict со следующими полями:
            - student - объект Student
            - subject_class - объект SubjectClass
            - mark - str с целым числом
            - attendance - str"""
    new_ceil = _insertNewDataInJournalCeil(JournalCeil(), validated_data)
    new_ceil.save()


def updateExistingJournalCeil(validated_data, ceil_id):
    """Обновить существующую в базе данных ячейку
    input:
        ceil_id -> id ячейки в таблице
        validated_data -> dict со следующими полями:
            - student -> объект Student
            - subject_class -> объект SubjectClass
            - mark -> str с целым числом
            - attendance -> str
    output:
        Exception -> в случае ошибки"""
    journal_ceil = getJournalCeil(ceil_id)
    journal_ceil = _insertNewDataInJournalCeil(journal_ceil, validated_data)
    journal_ceil.save()


def deleteJournalCeilFromDb(ceil_id):
    """Удалить ячейку из базы данных по ceil_id
    input:
        ceil_id -> id ячейки в таблице
    output:
        Exception -> в случае ошибки"""
    journal_ceil = getJournalCeil(ceil_id)
    journal_ceil.delete()

        


