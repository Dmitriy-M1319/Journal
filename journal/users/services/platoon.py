"""
Модуль бизнес-логики для взвода
"""
from django.db.models import ObjectDoesNotExist, QuerySet

from timetable.services import get_platoon_timetable_on_day
from users.models import Platoon
from utils.services import get_all_days_in_this_month


def get_platoon_by_number(platoon_number: int) -> Platoon:
    try:
         return Platoon.objects.get(platoon_number=platoon_number)
    except ObjectDoesNotExist:
        raise ValueError('Взвода с таким номером не существует в базе')


def get_students_by_platoon(platoon_number: int) -> QuerySet:
    platoon = get_platoon_by_number(platoon_number)
    return platoon.studentprofile_set.filter(active='учится').order_by('surname')


def create_timetable_for_platoon(platoon_number: int) -> list:
    platoon = get_platoon_by_number(platoon_number)
    month_days = get_all_days_in_this_month(platoon.study_day)
    all_timetable = list()
    for day in month_days:
        all_timetable.append(get_platoon_timetable_on_day(platoon, day))
    return all_timetable


def graduate_platoon(platoon_number: int) -> None:
    platoon = get_platoon_by_number(platoon_number)
    platoon.status = 'выпустился'
    platoon.save()

