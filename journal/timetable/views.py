from django.http import JsonResponse
from users.models import *
from .timetable_service import getDateFromRequest, getPlatoonTimetable, getSubject
from users.platoon_services import getPlatoonByNumber
from users.teacher_services import getTeacher
from journal.encoders import SubjectClassEncoder, SubjectEncoder

import logging

logger = logging.getLogger(__name__)

def getTimetableForPlatoonInDay(request, id):
    """Получить расписание для своего взвода на определенный день"""
    try:
        platoon = getPlatoonByNumber(id)
        class_day = getDateFromRequest(request)
        timetable = getPlatoonTimetable(platoon, class_day)
        return JsonResponse(timetable)
    except Exception as e:
        return JsonResponse({'timetable': None, 'message': e})


def getSubjectsForTeacher(request, id):
    """ Получить для преподавателя с идентификатором id список предметов, которые он ведет """
    try:
        teacher = getTeacher(id)
        subjects = teacher.subject_set.all()
        logger.info(f'get subjects for teacher with id {id}')
        return JsonResponse({'subjects': subjects}, safe=False, encoder=SubjectEncoder)
    except Exception as e:
        return JsonResponse({'subjects': None, 'message': e})


def getSubjectClassesForTeacher(request, id):
    """ Получить все занятия по предмету с номером subject_id, который ведет преподаватель с идентификатором id """
    try:
        teacher = getTeacher(id) 
        subject = getSubject(request.GET.get('subject_id'))

        # TODO: придумать в сервисах проверку на наличие данного предмета в списке предметов преподавателя
        if not teacher.subject_set.filter(name=subject.name):
            return JsonResponse({'subject_classes': None, 'message': 'Данный предмет не ведется преподавателем'})

        subject_classes = subject.subject_class_set.all()
        logger.info(f'get subject classes for teacher with id {id}')
        return JsonResponse({'subject_classes': subject_classes}, safe=False, encoder=SubjectClassEncoder)
    except Exception as e:
        return JsonResponse({'subject_classes': None, 'message': e})



