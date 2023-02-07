from django.http import JsonResponse
from users.models import *
from .timetable_service import *
from users.platoon_services import getPlatoonByNumber
from users.teacher_services import getTeacher
from journal.encoders import SubjectClassEncoder, SubjectEncoder

import logging

logger = logging.getLogger(__name__)

def getTimetableForPlatoonInDay(request, id):
    """Получить расписание для своего взвода на определенный день"""
    try:
        platoon = getPlatoonByNumber(id)
        class_day = getDateFromStr(request.GET.get('day'))
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
        if not teacher.subject_set.filter(name=subject.name):
            return JsonResponse({'subject_classes': None, 'message': 'Данный предмет не ведется преподавателем'})

        subject_classes = subject.subject_class_set.all()
        logger.info(f'get subject classes for teacher with id {id}')
        return JsonResponse({'subject_classes': subject_classes}, safe=False, encoder=SubjectClassEncoder)
    except Exception as e:
        return JsonResponse({'subject_classes': None, 'message': e})


def _getValidatedDataForSubjectFromRequest(request):
    data = {'teacher': request.POST.get('teacher'), 'name': request.POST.get('name'), 'hours': request.POST.get('hours'),
                'teacher': request.POST.get('teacher'), 'form': request.POST.get('form')}
    validated_data = validateSubjectData(data)
    return validated_data


def addSubject(request):
    if request.method == 'POST':
        try:
            validated_data = _getValidatedDataForSubjectFromRequest(request)
            addSubjectToDb(validated_data)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e})


def updateSubject(request, id):
    if request.method == 'POST':
        try:
            validated_data = _getValidatedDataForSubjectFromRequest(request)
            updateSubjectInDb(validated_data, id)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e})


def deleteSubject(request, id):
    if request.method == 'POST':
        try:
            deleteSubjectFromDb(id)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e})


def _getDataForSubjectClassFromRequest(request):
    data = {'subject': request.POST.get('subject'), 'platoon': request.POST.get('platoon'), 'class_date': request.POST.get('class_date'),
            'theme_number': request.POST.get('theme_number'),'theme_name': request.POST.get('theme_name'), 'class_number': request.POST.get('class_number'),
            'class_name': request.POST.get('class_name'), 'class_type': request.POST.get('class_type'), 'classroom': request.POST.get('classroom')}
    validated_data = validateSubjectData(data)
    return validated_data


def addSubjectClass(request):
    if request.method == 'POST':
        try:
            validated_data = _getDataForSubjectClassFromRequest(request)
            addSubjectClassToDb(validated_data)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e})


def updateSubjectClass(request, id):
    if request.method == 'POST':
        try:
            validated_data = _getDataForSubjectClassFromRequest(request)
            updateSubjectClassInDb(validated_data, id)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e})


def deleteSubjectClass(request, id):
    if request.method == 'POST':
        try:
            deleteSubjectClassFromDb(id)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e})


