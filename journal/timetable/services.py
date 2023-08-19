"""
Модуль, предоставляющий сервисы для работы с расписанием и занятиями
"""
from datetime import date

from django.db.models import ObjectDoesNotExist, QuerySet

from users.models import Platoon, StudentProfile, TeacherProfile 
from .serializers import SubjectClassSerializer, SubjectCreateSerializer
from .models import DirectionsSubjects, SubjectClass, Subject


def get_platoon_timetable_on_day(platoon: Platoon, local_day: date):
    classes = platoon.subjectclass_set.filter(class_date__day=local_day.day,
                                              class_date__month=local_day.month,
                                              class_date__year=local_day.year).order_by('class_date')
    if not classes:
        classes = []
    return {'date': local_day.strftime("%d.%m.%Y"), 'classes': SubjectClassSerializer(classes, many=True).data}


def get_classes_by_platoon_and_subject(platoon: Platoon, subject: Subject):
     return SubjectClass.objects.filter(platoon=platoon, subject=subject)
        

def get_subject(subject_id) -> Subject:
    try:
        subject = Subject.objects.get(id=subject_id)
        return subject
    except ObjectDoesNotExist:
        raise ValueError("Такого предмета не существует в базе")


def create_subject(data: dict) -> Subject:
    serializer = SubjectCreateSerializer(daya=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

    
def get_subject_for_student(student: StudentProfile) -> list[Subject]:
    dir_subjs = DirectionsSubjects.objects.filter(course_direction=student.platoon.course)
    subjects = list()
    for ds in dir_subjs:
        subjects.append(ds.subject)
    return subjects


def get_subject_class(id) -> SubjectClass:
    try:
        subject_class = SubjectClass.objects.get(id=id)
        return subject_class
    except ObjectDoesNotExist:
        raise ValueError("Такого занятия не существует в базе")


def get_subject_classes_by_subject(subject_id) -> QuerySet:
    current_subject = get_subject(subject_id)
    return current_subject.subjectclass_set.order_by('id')


def get_subject_classes_for_teacher(teacher: TeacherProfile, subject_id: int):
    subject = get_subject(subject_id)
    if not teacher.subject_set.filter(name=subject.name):
        raise ValueError('Данный предмет не ведется преподавателем')
    return subject.subjectclass_set.all()


def get_timetable_for_teacher_by_day(teacher: TeacherProfile, day: date):
    subjects = Subject.objects.filter(teacher=teacher)
    classes = SubjectClass.objects.filter(subject__in=subjects,
                                          class_date__day=day.day,
                                          class_date__month=day.month,
                                          class_date__year=day.year).order_by('class_date')
    dates = dict()
    for cl in classes:
        date_str = cl.class_date.strftime('%d.%m.%Y')
        if date_str not in dates:
            dates[date_str] = list()
        dates[date_str].append(cl)
    result = list()
    for key in dates:
        result.append({'date': key, 'classes': SubjectClassSerializer(dates[key], many=True).data})
    return result


def get_classes_dates_by_teacher_and_year(year, teacher: TeacherProfile):
    ''' Получить список дней по месяцам в определенном году, 
    в которые у преподавателя есть занятия'''
    subjects = Subject.objects.filter(teacher=teacher)
    classes = SubjectClass.objects.filter(subject__in=subjects)
    result = {'dates': list()}
    for month in range(1, 13):
        these_subjects = classes.filter(class_date__month=month) & classes.filter(class_date__year=year)
        result['dates'].append({'month': month, 'days': these_subjects.values_list('class_date__day', flat=True)})
    return result

