"""
Модуль бизнес-логики для взвода
"""
from django.db.models import QuerySet
from timetable.timetable_service import get_all_days_in_this_month, get_platoon_timetable
from users.models import Platoon, StudentProfile


def get_platoon_by_number(platoon_number: int) -> Platoon:
    """ 
    Получить взвод по номеру platoon_number
    """
    try:
        platoon = Platoon.objects.get(platoon_number=platoon_number)
        return platoon
    except:
        raise Exception('Взвода с таким номером не существует в базе')


def get_students_by_platoon(platoon_number: int) -> QuerySet:
    """
    Получить список студентов взвода с номером platoon_number 
    """
    platoon = get_platoon_by_number(platoon_number)
    students = StudentProfile.objects.filter(platoon=platoon)
    students = students.filter(active='study')
    return students


def create_timetable_for_platoon(platoon_number: int):
    """
    Составить расписание для взвода
    """
    platoon = get_platoon_by_number(platoon_number)
    month_days = get_all_days_in_this_month(platoon.study_day)
    all_timetable = list()
    for day in month_days:
        timetable = get_platoon_timetable(platoon, day)
        all_timetable.append(timetable)
    return all_timetable


def graduate_platoon(platoon_number: int):
    """ 
    Выпустить взвод 
    """
    platoon = get_platoon_by_number(platoon_number)
    platoon.status = 'выпустился'
    platoon.save()

