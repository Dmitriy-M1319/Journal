"""
Модуль вспомогательных сервисов
"""
import re
import datetime
from datetime import date

from django.core.handlers.base import transaction
from django.core.serializers.json import json
from django.db.backends.utils import functools
from rest_framework.response import Response


_date_pattern = r'\d{4}-\d{2}-\d{2}'


def load_post_data(request) -> dict:
    """
    Загрузить тело запроса из самого HTTP-запроса
    """
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    return body_data


def get_all_days_in_this_month(day_type) -> list:
    """
    Получить все определенные дни текущего месяца
    """
    year = date.today().year
    month = date.today().month
    day_of_week = day_type  # 0 - понедельник, 1 - вторник, и т.д.

    first_day = datetime.date(year, month, 1)
    delta = (day_of_week - first_day.weekday()) % 7
    first_monday = first_day + datetime.timedelta(days=delta)

    days = []
    current_day = first_monday
    while current_day.month == month:
        days.append(current_day)
        current_day += datetime.timedelta(weeks=1)
    return days


def get_date_from_str(local_date: str) -> date:
    """
    Выделить дату из строки local_date
    """
    if not re.fullmatch(_date_pattern, local_date):
        raise Exception("Некорректные данные для даты")
    else:
        date_lst = local_date.split('-')
        return date(int(date_lst[0]), int(date_lst[1]), int(date_lst[2]))


def get_date_and_time_from_str(date_time: str) -> datetime.datetime:
    """ 
    Преобразовать дату и время в виде строки в объект datetime
    """
    local_datetime = date_time.split('T')
    local_date = get_date_from_str(local_datetime[0])
    time_lst = local_datetime[1].split(':')
    return datetime.datetime(local_date.year, 
                             local_date.month, 
                             local_date.day, 
                             int(time_lst[0]), 
                             int(time_lst[1]))



def base_exception(status_code=400):
    """
    Декоратор для обработки исключения получения ошибки из сервисов
    """
    def exception_decorator(func):
        @functools.wraps(func)
        def instance(request, *args, **kwargs):
            try:
                with transaction.atomic():
                    return func(request, *args, **kwargs)
            except Exception as e:
                return Response({'detail': e.__str__()}, status=status_code)
        return instance
    return exception_decorator
