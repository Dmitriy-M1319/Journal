from django.http import JsonResponse
from journal.encoders import *
from journal.base_view import baseView
from users.platoon_services import addNewPlatoon, deletePlatoonWithGraduation, getPlatoonByNumber, validateDataForPlatoon
from .teacher_services import addNewTeacherToDatabase, deleteTeacherFromDatabase, updateExistingTeacher, validateTeacherData
from .student_services import *
from .models import *
import logging


logger = logging.getLogger(__name__)


def _getValidatedStudentData(request):
    data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
            'sex': request.POST.get('sex'), 'military_post': request.POST.get('military_post'), 'platoon': request.POST.get('platoon'),
            'login': request.POST.get('login'), 'password': request.POST.get('password'), 'department': request.POST.get('department'),
            'group_number': request.POST.get('group_number')}
    return validateStudentData(data)


@baseView
def createStudent(request):
    """Добавить студента на кафедру"""
    if request.method == 'POST':
        data = _getValidatedStudentData(request)
        validateStudentData(data)
        addNewStudent(data)
        return JsonResponse({'success': True}) 
            

@baseView
def updateStudent(request, id):
    """Обновить данные студента на кафедре"""
    if request.method == 'POST':
        data = _getValidatedStudentData(request)
        validateStudentData(data)
        updateStudentInDb(data, id)
        return JsonResponse({'success': True}) 


@baseView
def deleteStudent(request, id):
    """ 'Отчислить' студента с кафедры """
    if request.method == 'POST':
        deleteStudentFromDb(id)
        logger.info(f'student with id {id} was removed succesfully')
        return JsonResponse({'success': True}) 


def _getValidatedTeacherData(request):
    data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
            'military_post': request.POST.get('military_post'), 'military_rank': request.POST.get('military_rank'), 'cycle': request.POST.get('cycle'),
            'role': request.POST.get('role'), 'login': request.POST.get('login'), 'password': request.POST.get('password')}
    return validateTeacherData(data)


@baseView
def createTeacher(request):
    """Веб-сервис, предоставляющий занесение приглашенного преподавателя в базу"""
    if request.method == 'POST':
        data = _getValidatedTeacherData(request)
        validateTeacherData(data)
        addNewTeacherToDatabase(data)
        return JsonResponse({'success': True}) 


@baseView
def updateTeacher(request, id):
    """Веб-сервис, предоставляющий обновление информации о преподавателе"""
    if request.method == 'POST':
        data = _getValidatedTeacherData(request)
        validateTeacherData(data)
        updateExistingTeacher(data, id)
        return JsonResponse({'success': True}) 


@baseView
def deleteTeacher(request, id):
    """Веб-сервис, предоставляющий увольнение преподавателей с кафедры"""
    if request.method == 'POST':
        deleteTeacherFromDatabase(id)
        logger.info(f'teacher with id {id} was removed succesfully')
        return JsonResponse({'success': True}) 


@baseView
def getPlatoonByStudent(request, id):
    """Получить объект взвода, в котором находится студент с номером id"""
    platoon = getStudent(id).platoon
    logger.info(f"get correct platoon for student with id {id}")
    return JsonResponse(platoon, safe=False, encoder=PlatoonEncoder)


@baseView
def getStudentsByPlatoon(request, id):
    """ Получить список студентов по номеру взвода, который представлен id """
    platoon = getPlatoonByNumber(id)
    students = platoon.student_set.all()
    logger.info(f'get students from platoon with platoon number {id}')
    return JsonResponse({'students': students}, safe=False, encoder=StudentEncoder)


@baseView
def getPlatoonTutor(request, id):
    """Получение куратора взвода с номером id"""
    platoon = getPlatoonByNumber(id)
    tutor = platoon.tutor
    if not tutor:
        logger.error(f'platoon with platoon_number {id} does not have a tutor')
        return JsonResponse({'tutor': None, 'message': 'У данного взвода нет куратора'})
    logger.info(f'get tutor of platoon with platoon number {id}')
    return JsonResponse({'tutor': tutor}, safe=False, encoder=TeacherEncoder)


def _getValidatedPlatoonData(request):
    data = {'platoon_number': request.POST.get('platoon_number'), 'tutor': request.POST.get('tutor'), 'year': request.POST.get('year'),
            'status': request.POST.get('status')}
    return validateDataForPlatoon(data)


@baseView
def createPlatoon(request):
    """Добавление нового взвода на кафедру"""
    if request.method == 'POST':
        addNewPlatoon(_getValidatedPlatoonData(request))
        platoon_number = request.POST.get('platoon_number')
        logger.info(f'create a new platoon with platoon number {platoon_number}')
        return JsonResponse({'success': True}) 


@baseView
def updatePlatoon(request, id):
    """Обновление данных существующего взвода на кафедре"""
    if request.method == 'POST':
        data = {'platoon_number': request.POST.get('platoon_number'), 'tutor': request.POST.get('tutor'), 'year': request.POST.get('year'),
                'status': request.POST.get('status')}
        result = validateDataForPlatoon(data)
        updatePlatoon(result, id)
        logger.info(f'update a platoon with platoon number {id}')
        return JsonResponse({'success': True}) 


@baseView
def deletePlatoon(request, id):
    """ 'Выпуск' взвода с кафедры """
    if request.method == 'POST':
        deletePlatoonWithGraduation(id)
        logger.info(f'delete a platoon with platoon number {id}')
        return JsonResponse({'success': True})
