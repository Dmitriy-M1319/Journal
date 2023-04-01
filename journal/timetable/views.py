from django.core.serializers.json import json
from django.http import JsonResponse
from journal.base_view import baseView
from users.models import *
from .timetable_service import *
from users.platoon_services import get_platoon_by_number
from users.teacher_services import get_teacher
from journal.encoders import SubjectClassEncoder, SubjectEncoder
from django.views.decorators.csrf import ensure_csrf_cookie

import logging

logger = logging.getLogger(__name__)

@baseView
def getTimetableForPlatoonInDayView(request, id): # не работает фильтр по времени
    """Получить расписание для своего взвода на определенный день"""
    logger.info('GET: get timetable for platoon')
    platoon = get_platoon_by_number(id)
    class_day = getDateFromStr(request.GET.get('day'))
    timetable = getPlatoonTimetable(platoon, class_day)
    return JsonResponse(timetable)


@baseView
def getSubjectsForTeacherView(request, id): # работает
    """ Получить для преподавателя с идентификатором id список предметов, которые он ведет """
    logger.info('GET: get subject list for teacher')
    teacher = get_teacher(id)
    subjects = teacher.subject_set.all()
    logger.info(f'get subjects for teacher with id {id}')
    return JsonResponse(convertSubjectsToJson(subjects), safe=False, encoder=SubjectEncoder)


@baseView
def getSubjectClassesForTeacherView(request, id): # работает
    """ Получить все занятия по предмету с номером subject_id, который ведет преподаватель с идентификатором id """
    logger.info('GET: get subject class list for teacher')
    teacher = get_teacher(id) 
    subject = getSubject(request.GET.get('subject_id'))
    if not teacher.subject_set.filter(name=subject.name):
        return JsonResponse({'subject_classes': None, 'message': 'Данный предмет не ведется преподавателем'})

    subject_classes = subject.subjectclass_set.all()
    logger.info(f'get subject classes for teacher with id {id}')
    return JsonResponse(convertSubjectClassesToJson(subject_classes), safe=False, encoder=SubjectClassEncoder)



@baseView
@ensure_csrf_cookie
def createSubjectView(request):
    if request.method == 'POST':
        logger.info('POST: create new subject')
        addSubjectToDb(validateSubjectData(json.loads(request.body)))
        return JsonResponse({'success': True})


@baseView
@ensure_csrf_cookie
def updateSubjectView(request, id):
    if request.method == 'POST':
        logger.info('POST: update existing subject with id {id}')
        updateSubjectInDb(validateSubjectData(json.loads(request.body)), id)
        return JsonResponse({'success': True})


@baseView
@ensure_csrf_cookie
def deleteSubjectView(request, id):
    if request.method == 'POST':
        logger.info('POST: remove existing subject with id {id}')
        deleteSubjectFromDb(id)
        return JsonResponse({'success': True})


@baseView
@ensure_csrf_cookie
def createSubjectClassView(request):
    if request.method == 'POST':
        logger.info('POST: create new subject class')
        addSubjectClassToDb(validateSubjectClassData(json.loads(request.body)))
        return JsonResponse({'success': True})


@baseView
@ensure_csrf_cookie
def updateSubjectClassView(request, id):
    if request.method == 'POST':
        logger.info('POST: update existing subject class with id {id}')
        updateSubjectClassInDb(validateSubjectClassData(json.loads(request.body)), id)
        return JsonResponse({'success': True})


@baseView
@ensure_csrf_cookie
def deleteSubjectClassView(request, id):
    if request.method == 'POST':
        logger.info('POST: remove existing subject class with id {id}')
        deleteSubjectClassFromDb(id)
        return JsonResponse({'success': True})


