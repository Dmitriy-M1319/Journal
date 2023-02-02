from django.http import JsonResponse
from users.models import *
from .timetable_service import getTimetableForPlatoon
from journal.encoders import SubjectClassEncoder, SubjectEncoder
import logging

logger = logging.getLogger(__name__)

def getTimetable(request, id):
    """Получить расписание для своего взвода"""
    student = Student.objects.get(id=id)
    if not student:
        logger.error(f"student with id {id} doesn't exist")
        return JsonResponse({"timetable": None})

    timetable = getTimetableForPlatoon(student.platoon.id)
    if not timetable:
        logger.error(f"the timetable for platoon {student.platoon.id} is impossible")
        return JsonResponse({"timetable": None})
    else:
        logger.info(f'get timetable for student {id}')
        return JsonResponse(timetable)


def getSubjectsForTeacher(request, id):
    """ Получить для преподавателя с идентификатором id список предметов, которые он ведет """
    teacher = Teacher.objects.get(id=id)
    if not teacher:
        logger.error(f'teacher with id {id} doesn\'t exist')
        return JsonResponse({'subjects': None, 'message': 'Такого преподавателя не существует в базе'})

    subjects = teacher.subject_set.all()
    logger.info(f'get subjects for teacher with id {id}')
    return JsonResponse({'subjects': subjects}, safe=False, encoder=SubjectEncoder)


def getSubjectClassesForSubject(request, id):
    """ Получить все занятия по предмету, который ведет преподаватель """
    teacher = Teacher.objects.get(id=id)
    if not teacher:
        logger.error(f'teacher with id {id} doesn\'t exist')
        return JsonResponse({'subject_classes': None, 'message': 'Такого преподавателя не существует в базе'})

    subject = teacher.subject_set.filter(id=request.GET.get('subject_id'))

    if not subject:
        s_id = request.GET.get('subject_id')
        logger.error(f'subject with id {s_id} doesn\'t exist')
        return JsonResponse({'subject_classes': None, 'message': 'Такого предмета для данного преподавателя не существует в базе'})

    subject_classes = subject.subject_class_set.all()
    logger.info(f'get subject classes for teacher with id {id}')
    return JsonResponse({'subject_classes': subject_classes}, safe=False, encoder=SubjectClassEncoder)



