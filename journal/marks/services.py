"""
Модуль бизнес-логики для работы с оценками в электронном журнале
"""
from django.dispatch import receiver
from django.db.models.signals import post_save

from marks.models import JournalCeil
from users.services.platoon import get_students_by_platoon
from timetable.services import *
from users.serializers import StudentProfileSerializer
from .serializers import CeilSerializer

def get_journal_ceil(journal_id):
    """
    Получает объект ячейки по его id
    """
    try:
        ceil = JournalCeil.objects.get(id=journal_id)
        return ceil
    except:
        raise Exception('Такой ячейки не существует')


def get_ceils_by_platoon_and_subject(subject_id, platoon):
    """
    Получить оценки взвода по определенному предмету
    """
    students = get_students_by_platoon(platoon)
    platoon_classes = get_classes_by_platoon_and_subject(platoon, subject_id)
    ceils = list()
    for student in students:
        student_ceils = JournalCeil.objects.filter(subject_class__in=platoon_classes, student=student) 
        ceils.append({'student': StudentProfileSerializer(student).data, 'marks': CeilSerializer(student_ceils, many=True).data})
    return ceils


def create_column_for_class(subjects_class: SubjectClass):
    """
    Создать 'пустые' ячейки оценок для взвода по определенному занятию
    """
    students = get_students_by_platoon(subjects_class.platoon.platoon_number)
    for student in students:
        JournalCeil.objects.create(student=student, subject_class=subjects_class, mark=0, attendance='')


@receiver(post_save, sender=SubjectClass)
def create_journal_ceils(sender, instance, created, **kwargs):
    if created:
        create_column_for_class(instance)


def get_ceils_for_student_by_subject(student: StudentProfile, subject: Subject):
    """
    Получить список оценок для студента
    """
    journal_ceils = JournalCeil.objects.filter(student=student, 
                                               subject_class__subject=subject).order_by('subject_class__class_date')
    return journal_ceils

