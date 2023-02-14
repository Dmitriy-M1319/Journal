from django.http import JsonResponse
from journal.base_view import baseView
from users.models import *
from .timetable_service import *
from users.platoon_services import getPlatoonByNumber
from users.teacher_services import getTeacher
from journal.encoders import SubjectClassEncoder, SubjectEncoder

import logging

logger = logging.getLogger(__name__)

@baseView
def getTimetableForPlatoonInDayView(request, id):
    """Получить расписание для своего взвода на определенный день"""
    platoon = getPlatoonByNumber(id)
    class_day = getDateFromStr(request.GET.get('day'))
    timetable = getPlatoonTimetable(platoon, class_day)
    return JsonResponse(timetable)


@baseView
def getSubjectsForTeacherView(request, id):
    """ Получить для преподавателя с идентификатором id список предметов, которые он ведет """
    teacher = getTeacher(id)
    subjects = teacher.subject_set.all()
    logger.info(f'get subjects for teacher with id {id}')
    return JsonResponse({'subjects': subjects}, safe=False, encoder=SubjectEncoder)


@baseView
def getSubjectClassesForTeacherView(request, id):
    """ Получить все занятия по предмету с номером subject_id, который ведет преподаватель с идентификатором id """
    teacher = getTeacher(id) 
    subject = getSubject(request.GET.get('subject_id'))
    if not teacher.subject_set.filter(name=subject.name):
        return JsonResponse({'subject_classes': None, 'message': 'Данный предмет не ведется преподавателем'})

    subject_classes = subject.subject_class_set.all()
    logger.info(f'get subject classes for teacher with id {id}')
    return JsonResponse({'subject_classes': subject_classes}, safe=False, encoder=SubjectClassEncoder)


def _getValidatedDataForSubjectFromRequest(request):
    data = {'teacher': request.POST.get('teacher'), 'name': request.POST.get('name'), 'hours': request.POST.get('hours'),
                'teacher': request.POST.get('teacher'), 'form': request.POST.get('form')}
    return validateSubjectData(data)


@baseView
def createSubjectView(request):
    if request.method == 'POST':
        addSubjectToDb(_getValidatedDataForSubjectFromRequest(request))
        return JsonResponse({'success': True})


@baseView
def updateSubjectView(request, id):
    if request.method == 'POST':
        updateSubjectInDb(_getValidatedDataForSubjectFromRequest(request), id)
        return JsonResponse({'success': True})


@baseView
def deleteSubjectView(request, id):
    if request.method == 'POST':
        deleteSubjectFromDb(id)
        return JsonResponse({'success': True})


def _getDataForSubjectClassFromRequest(request):
    data = {'subject': request.POST.get('subject'), 'platoon': request.POST.get('platoon'), 'class_date': request.POST.get('class_date'),
            'theme_number': request.POST.get('theme_number'),'theme_name': request.POST.get('theme_name'), 'class_number': request.POST.get('class_number'),
            'class_name': request.POST.get('class_name'), 'class_type': request.POST.get('class_type'), 'classroom': request.POST.get('classroom')}
    return validateSubjectData(data)


@baseView
def createSubjectClassView(request):
    if request.method == 'POST':
        addSubjectClassToDb(_getDataForSubjectClassFromRequest(request))
        return JsonResponse({'success': True})


@baseView
def updateSubjectClassView(request, id):
    if request.method == 'POST':
        updateSubjectClassInDb(_getDataForSubjectClassFromRequest(request), id)
        return JsonResponse({'success': True})


@baseView
def deleteSubjectClassView(request, id):
    if request.method == 'POST':
        deleteSubjectClassFromDb(id)
        return JsonResponse({'success': True})


