"""
Модуль, предоставляющий сервисы для работы с расписанием и занятиями
"""
import re
from datetime import date, datetime
from .serializers import SubjectClassSerializer
from users.student_services import get_student
from users.platoon_services import get_platoon_by_number
from .models import DirectionsSubjects, SubjectClass, Subject


_date_pattern = r'\d{4}-\d{2}-\d{2}'


def get_platoon_timetable(platoon_number, day):
    """Составить расписание для взвода platoon на определенный день day"""
    platoon = get_platoon_by_number(platoon_number)
    local_day = get_date_from_str(day)
    print(local_day)
    classes = platoon.subjectclass_set.filter(class_date__day=local_day.day,
                                              class_date__month=local_day.month,
                                              class_date__year=local_day.year).order_by('class_date')
    if not classes:
        raise Exception("У данного взвода нет занятий в этот день")
    else:
        return classes


def get_classes_by_platoon_and_subject(platoon_number, subject):
    """ Получить все занятия для взвода по определенному предмету """
    classes = SubjectClass.objects.find(platoon=platoon_number, subject=subject)
    return classes
        

def get_date_from_str(local_date:str):
    """Выделить дату из строки local_date"""
    if not re.fullmatch(_date_pattern, local_date):
        raise Exception("Некорректные данные для даты")
    else:
        date_lst = local_date.split('-')
        return date(int(date_lst[0]), int(date_lst[1]), int(date_lst[2]))


def get_subject(subject_id) -> Subject:
    """ Получить экземпляр предмета по его id"""
    subject = Subject.objects.get(id=subject_id)
    if not subject:
        raise Exception("Такого предмета не существует в базе")
    else:
        return subject


def get_subject_for_student(student_id):
    """ Получить список текущих предметов для студента """
    student = get_student(student_id)
    course = student.platoon.course
    dir_subjs = DirectionsSubjects.objects.filter(course_direction=course)
    subjects = list()
    for ds in dir_subjs:
        subjects.append(ds.subject)
    print(subjects)
    return subjects


def get_subject_class(id):
    """ Получить экземпляр занятия по его id"""
    subject_class = SubjectClass.objects.get(id=id)
    if not subject_class:
        raise Exception("Такого занятия не существует в базе")
    else:
        return subject_class


def get_subject_classes_by_subject(subject_id):
    """Получить все занятия по определенному предмету с номером id"""
    current_subject = get_subject(subject_id)
    subject_classes = SubjectClass.objects.filter(subject=current_subject).order_by('id')
    return subject_classes.values()


def get_timetable_for_teacher(teacher): 
    """Получить все занятия для преподавателя, группируя по датам"""
    subjects = Subject.objects.filter(teacher=teacher)
    classes = SubjectClass.objects.filter(subject__in=subjects)
    dates = dict()
    for cl in classes:
        if cl.class_date.month < 10:
            month = '0' + str(cl.class_date.month)
        else:
            month = str(cl.class_date.month)
        key = f'{cl.class_date.day}.{month}.{cl.class_date.year}'
        if key in dates:
            dates[key].append(cl)
        else:
            dates[key] = list()
            dates[key].append(cl)
    result = list()
    for key in dates:
        result.append({'date': key, 'classes': SubjectClassSerializer(dates[key], many=True).data})
    return result


def get_date_and_time_from_str(date_time:str):
    """ Преобразовать дату и время в виде строки в объект datetime
    input:
        date_time -> str с датой и временем в формате ГГГГ-ММ-ДДTЧЧ:ММ"""
    local_datetime = date_time.split('T')
    local_date = get_date_from_str(local_datetime[0])
    time_lst = local_datetime[1].split(':')
    return datetime(local_date.year, local_date.month, local_date.day, int(time_lst[0]), int(time_lst[1]))
