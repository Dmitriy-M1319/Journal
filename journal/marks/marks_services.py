"""
Модуль бизнес-логики для работы с оценками в электронном журнале
"""
from marks.models import JournalCeil
from users.student_services import get_student
from users.platoon_services import get_students_by_platoon
from timetable.timetable_service import *
from users.serializers import StudentProfileSerializer
from .serializers import CeilSerializer

def get_journal_ceil(journal_id):
    """Получает объект ячейки по его id"""
    try:
        ceil = JournalCeil.objects.get(id=journal_id)
        return ceil
    except:
        raise Exception('Такой ячейки не существует')


def get_ceils_by_platoon_and_subject(subject_id, platoon_number):
    """ Получить оценки взвода по определенному предмету """
    students = get_students_by_platoon(platoon_number)
    platoon_classes = get_classes_by_platoon_and_subject(platoon_number, subject_id)
    ceils = dict()
    for student in students:
       student_ceils = JournalCeil.objects.filter(subject_class__in=platoon_classes, student=student) 
       ceils[StudentProfileSerializer(student).data] = CeilSerializer(student_ceils, many=True).data
    return ceils


def get_ceils_for_student(student_id):
    """Получить список оценок для студента по student_id
    input:
        student_id -> id студента
    output:
        list с объектами JournalCeil -> список ячеек
        Exception -> в случае ошибки"""
    current_student = get_student(student_id)
    journal_ceils = JournalCeil.objects.filter(student=current_student).order_by('id')
    return journal_ceils.values()

