import logging
from django.core.serializers.json import json

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from journal.encoders import *
from journal.base_view import baseView
from .platoon_services import *
from .teacher_services import *
from .student_services import *
from .models import *


logger = logging.getLogger(__name__)


@baseView
def getStudentByIdView(request, id):
    """Веб-сервис, предоставляющий получение студента по его id"""
    student = get_student(id)
    return JsonResponse(student, safe=False, encoder=StudentEncoder)


@baseView
def createStudentView(request):
    """Добавить студента на кафедру"""
    if request.method == 'POST':
        logger.info("POST: create new student")
        add_new_student_to_db(validate_student_data(json.loads(request.body)))
        return JsonResponse({'success': True}) 
            

@baseView
def updateStudentView(request, id):
    """Обновить данные студента на кафедре"""
    if request.method == 'POST':
        logger.info("POST: update existing student")
        update_existing_student(validate_student_data(json.loads(request.body)), id)
        return JsonResponse({'success': True}) 


@baseView
def deleteStudentView(request, id):
    """ 'Отчислить' студента с кафедры """
    if request.method == 'POST':
        logger.info("POST: remove existing student")
        delete_student(id)
        return JsonResponse({'success': True}) 


@baseView
def getTeacherByIdView(request, id):
    """Веб-сервис, предоставляющий получение студента по его id"""
    teacher = get_teacher(id)
    return JsonResponse(teacher, safe=False, encoder=TeacherEncoder)


@baseView
@ensure_csrf_cookie
def createTeacherView(request):
    """Веб-сервис, предоставляющий занесение приглашенного преподавателя в базу"""
    if request.method == 'POST':
        logger.info("POST: create new teacher")
        body = request.body
        body_json = json.loads(body)
        add_new_teacher_to_db(validate_teacher_data(body_json))
        return JsonResponse({'body': body_json, 'Success': True}) 


@baseView
@ensure_csrf_cookie
def updateTeacherView(request, id):
    """Веб-сервис, предоставляющий обновление информации о преподавателе"""
    if request.method == 'POST':
        logger.info("POST: update existing teacher")
        body = request.body
        body_json = json.loads(body)
        update_existing_teacher(validate_teacher_data(body_json), id)
        return JsonResponse({'success': True}) 


@baseView
@ensure_csrf_cookie
def deleteTeacherView(request, id):
    """Веб-сервис, предоставляющий увольнение преподавателей с кафедры"""
    if request.method == 'POST':
        logger.info("POST: remove existing teacher")
        delete_teacher(id)
        return JsonResponse({'success': True}) 


@baseView
def getPlatoonByNumberView(request, id):
    platoon = get_platoon_by_number(id)
    return JsonResponse(platoon, safe=False, encoder=PlatoonEncoder)


@baseView
def getPlatoonByStudentView(request, id):
    """Веб-сервис, предоставляющий получение объекта взвода, в котором состоит студент с номером id"""
    logger.info('GET: get platoon by student')
    platoon = get_student(id).studentprofile.platoon
    return JsonResponse(platoon, safe=False, encoder=PlatoonEncoder)


@baseView
def getStudentsByPlatoonView(request, id):
    """Веб-сервис, предоставляющий получение списка студентов взвода с номером id"""
    logger.info('GET: get list of students from platoon')
    platoon = get_platoon_by_number(id)
    students = platoon.student_set.all()
    return JsonResponse(convert_students_to_json(students), safe=False, encoder=StudentEncoder)


@baseView
def getPlatoonTutorView(request, id):
    """Веб-сервис, предоставляющий получение куратора взвода с номером id"""
    logger.info('GET: get platoon tutor')
    platoon = get_platoon_by_number(id)
    tutor = platoon.tutor
    if not tutor:
        return JsonResponse({'tutor': None, 'message': 'У данного взвода нет куратора'})
    return JsonResponse({'tutor': tutor}, safe=False, encoder=TeacherEncoder)



@baseView
def createPlatoonView(request):
    """Веб-сервис, предоставляющий добавление нового взвода на кафедру"""
    if request.method == 'POST':
        logger.info('POST: create new platoon')
        add_new_platoon_to_db(validate_platoon_data(json.loads(request.body)))
        return JsonResponse({'success': True}) 


@baseView
def updatePlatoonView(request, id):
    """Веб-сервис, предоставляющий обновление данных существующего взвода на кафедре"""
    if request.method == 'POST':
        logger.info('POST: update existing platoon')
        update_existing_platoon(validate_platoon_data(json.loads(request.body)), id)
        return JsonResponse({'success': True}) 


@baseView
def deletePlatoonView(request, id):
    """Веб-сервис, предоставляющий 'выпуск' взвода с кафедры """
    if request.method == 'POST':
        logger.info('POST: delete(graduate) existing platoon')
        delete_platoon(id)
        return JsonResponse({'success': True})
