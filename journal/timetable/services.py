"""
Модуль, предоставляющий сервисы для работы с расписанием и занятиями
"""

from datetime import date

from django.db.models import QuerySet
from users.services.teacher import get_teacher
from users.models import Platoon, StudentProfile, TeacherProfile, CourseDirection
from .serializers import SubjectClassSerializer
from .models import DirectionsSubjects, SubjectClass, Subject


def get_platoon_timetable(platoon: Platoon, local_day: date):
    """
    Составить расписание для взвода platoon на определенный день day
    """
    classes = platoon.subjectclass_set.filter(class_date__day=local_day.day,
                                              class_date__month=local_day.month,
                                              class_date__year=local_day.year).order_by('class_date')
    if not classes:
        if local_day.month < 10:
            m = '0' + str(local_day.month)
        else:
            m = str(local_day.month)
        key = f'{local_day.day}.{m}.{local_day.year}'
        return {'date': key, 'message' : "У данного взвода нет занятий в этот день"}
    else:
        if local_day.month < 10:
            m = '0' + str(local_day.month)
        else:
            m = str(local_day.month)            
        key = f'{local_day.day}.{m}.{local_day.year}'
        return {'date': key, 'classes': SubjectClassSerializer(classes, many=True).data}


def get_classes_by_platoon_and_subject(platoon: Platoon, subject: Subject):
    """
    Получить все занятия для взвода по определенному предмету
    """
    classes = SubjectClass.objects.filter(platoon=platoon, subject=subject)
    return classes
        

def get_subject(subject_id) -> Subject:
    """
    Получить экземпляр предмета по его id
    """
    subject = Subject.objects.get(id=subject_id)
    if not subject:
        raise Exception("Такого предмета не существует в базе")
    else:
        return subject


def create_subject(data: dict) -> Subject:
    """
    Создать новый предмет для направления обучения и курса
    """
    teacher = get_teacher(data['teacher'])
    subject = Subject.objects.create(name=data['name'],
                                    teacher=teacher,
                                    hours_count=data['hours_count'],
                                    form=data['form'])
    direction = CourseDirection.objects.get(id=data['direction'])
    DirectionsSubjects.objects.create(course_direction=direction, subject=subject)
    return subject


def get_subject_for_student(student: StudentProfile) -> list:
    """
    Получить список текущих предметов для студента
    """
    course = student.platoon.course
    dir_subjs = DirectionsSubjects.objects.filter(course_direction=course)
    subjects = list()
    for ds in dir_subjs:
        subjects.append(ds.subject)
    return subjects


def get_subject_class(id) -> SubjectClass:
    """
    Получить экземпляр занятия по его id
    """
    subject_class = SubjectClass.objects.get(id=id)
    if not subject_class:
        raise Exception("Такого занятия не существует в базе")
    else:
        return subject_class


def get_subject_classes_by_subject(subject_id) -> QuerySet:
    """
    Получить все занятия по определенному предмету с номером id
    """
    current_subject = get_subject(subject_id)
    subject_classes = SubjectClass.objects.filter(subject=current_subject).order_by('id')
    return subject_classes.values()


def get_subject_classes_for_teacher(teacher: TeacherProfile, subject_id: int):
    """
    Получить список занятий для данного преподавателя по определенному предмету
    """
    subject = get_subject(subject_id)
    if not teacher.subject_set.filter(name=subject.name):
        raise Exception('Данный предмет не ведется преподавателем')
    return subject.subjectclass_set.all()



def get_timetable_for_teacher(teacher: TeacherProfile): 
    """
    Получить все занятия для преподавателя, группируя по датам
    """
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
