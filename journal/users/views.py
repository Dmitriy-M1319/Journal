import logging

from django.http import JsonResponse
from journal.encoders import *
from journal.base_view import baseView
from .platoon_services import addNewPlatoon, deletePlatoonWithGraduation, getPlatoonByNumber, updateExistingPlatoon, validateDataForPlatoon
from .teacher_services import addNewTeacherToDatabase, deleteTeacherFromDatabase, updateExistingTeacher, validateTeacherData
from .student_services import *
from .models import *


logger = logging.getLogger(__name__)


def _getValidatedStudentData(request):
    data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
            'sex': request.POST.get('sex'), 'military_post': request.POST.get('military_post'), 'platoon': request.POST.get('platoon'),
            'login': request.POST.get('login'), 'password': request.POST.get('password'), 'department': request.POST.get('department'),
            'group_number': request.POST.get('group_number')}
    return validateStudentData(data)


@baseView
def createStudentView(request):
    """Добавить студента на кафедру"""
    if request.method == 'POST':
        logger.info("POST: create new student")
        addNewStudent(_getValidatedStudentData(request))
        return JsonResponse({'success': True}) 
            

@baseView
def updateStudentView(request, id):
    """Обновить данные студента на кафедре"""
    if request.method == 'POST':
        logger.info("POST: update existing student")
        updateStudentInDb(_getValidatedStudentData(request), id)
        return JsonResponse({'success': True}) 


@baseView
def deleteStudentView(request, id):
    """ 'Отчислить' студента с кафедры """
    if request.method == 'POST':
        logger.info("POST: remove existing student")
        deleteStudentFromDb(id)
        return JsonResponse({'success': True}) 


def _getValidatedTeacherData(request):
    data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
            'military_post': request.POST.get('military_post'), 'military_rank': request.POST.get('military_rank'), 'cycle': request.POST.get('cycle'),
            'role': request.POST.get('role'), 'login': request.POST.get('login'), 'password': request.POST.get('password')}
    return validateTeacherData(data)


@baseView
def createTeacherView(request):
    """Веб-сервис, предоставляющий занесение приглашенного преподавателя в базу"""
    if request.method == 'POST':
        logger.info("POST: create new teacher")
        addNewTeacherToDatabase(_getValidatedTeacherData(request))
        return JsonResponse({'success': True}) 


@baseView
def updateTeacherView(request, id):
    """Веб-сервис, предоставляющий обновление информации о преподавателе"""
    if request.method == 'POST':
        logger.info("POST: update existing teacher")
        updateExistingTeacher(_getValidatedTeacherData(request), id)
        return JsonResponse({'success': True}) 


@baseView
def deleteTeacherView(request, id):
    """Веб-сервис, предоставляющий увольнение преподавателей с кафедры"""
    if request.method == 'POST':
        logger.info("POST: remove existing teacher")
        deleteTeacherFromDatabase(id)
        return JsonResponse({'success': True}) 


@baseView
def getPlatoonByStudentView(request, id):
    """Веб-сервис, предоставляющий получение объекта взвода, в котором состоит студент с номером id"""
    logger.info('GET: get platoon by student')
    platoon = getStudent(id).platoon
    return JsonResponse(platoon, safe=False, encoder=PlatoonEncoder)


@baseView
def getStudentsByPlatoonView(request, id):
    """Веб-сервис, предоставляющий получение списка студентов взвода с номером id"""
    logger.info('GET: get list of students from platoon')
    platoon = getPlatoonByNumber(id)
    students = platoon.student_set.all()
    return JsonResponse({'students': students}, safe=False, encoder=StudentEncoder)


@baseView
def getPlatoonTutorView(request, id):
    """Веб-сервис, предоставляющий получение куратора взвода с номером id"""
    logger.info('GET: get platoon tutor')
    platoon = getPlatoonByNumber(id)
    tutor = platoon.tutor
    if not tutor:
        return JsonResponse({'tutor': None, 'message': 'У данного взвода нет куратора'})
    return JsonResponse({'tutor': tutor}, safe=False, encoder=TeacherEncoder)


def _getValidatedPlatoonData(request):
    data = {'platoon_number': request.POST.get('platoon_number'), 'tutor': request.POST.get('tutor'), 'year': request.POST.get('year'),
            'status': request.POST.get('status')}
    return validateDataForPlatoon(data)


@baseView
def createPlatoonView(request):
    """Веб-сервис, предоставляющий добавление нового взвода на кафедру"""
    if request.method == 'POST':
        logger.info('POST: create new platoon')
        addNewPlatoon(_getValidatedPlatoonData(request))
        return JsonResponse({'success': True}) 


@baseView
def updatePlatoonView(request, id):
    """Веб-сервис, предоставляющий обновление данных существующего взвода на кафедре"""
    if request.method == 'POST':
        logger.info('POST: update existing platoon')
        updateExistingPlatoon(_getValidatedPlatoonData(request), id)
        return JsonResponse({'success': True}) 


@baseView
def deletePlatoonView(request, id):
    """Веб-сервис, предоставляющий 'выпуск' взвода с кафедры """
    if request.method == 'POST':
        logger.info('POST: delete(graduate) existing platoon')
        deletePlatoonWithGraduation(id)
        return JsonResponse({'success': True})
