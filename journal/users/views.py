from django.http import JsonResponse

from journal.encoders import *
from journal.users.platoon_services import addNewPlatoon, deletePlatoonWithGraduation, getPlatoonByNumber, validateDataForPlatoon
from .teacher_services import addNewTeacherToDatabase, deleteTeacherFromDatabase, updateExistingTeacher, validateTeacherData
from .student_services import *
from .models import *
import logging


logger = logging.getLogger(__name__)

# API для студента
def createStudent(request):
    """Добавить студента на кафедру"""
    if request.method == 'POST':
        try:
            data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
                    'sex': request.POST.get('sex'), 'military_post': request.POST.get('military_post'), 'platoon': request.POST.get('platoon'),
                    'login': request.POST.get('login'), 'password': request.POST.get('password'), 'department': request.POST.get('department'),
                    'group_number': request.POST.get('group_number')}
            validateStudentData(data)
            addNewStudent(data)
            return JsonResponse({'success': True}) 
        except Exception as e:
            logger.error("The data for student creating is not corrected")
            return JsonResponse({'success': False, 'message': e})
            

def updateStudent(request, id):
    """Обновить данные студента на кафедре"""
    if request.method == 'POST':
        try:
            data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
                    'sex': request.POST.get('sex'), 'military_post': request.POST.get('military_post'), 'platoon': request.POST.get('platoon'),
                    'login': request.POST.get('login'), 'password': request.POST.get('password'), 'department': request.POST.get('department'),
                    'group_number': request.POST.get('group_number')}
            validateStudentData(data)
            updateStudentInDb(data, id)
            return JsonResponse({'success': True}) 
        except Exception as e:
            logger.error("The data for student updating is not corrected")
            return JsonResponse({'success': False, 'message': e})


def deleteStudent(request, id):
    """ 'Отчислить' студента с кафедры """
    if request.method == 'POST':
        try:
            deleteStudentFromDb(id)
            logger.info(f'student with id {id} was removed succesfully')
            return JsonResponse({'success': True}) 
        except Exception as e:
            logger.error(f'Failed to remove student with id {id}')
            return JsonResponse({'success': False, 'message': e})


# API для преподавателей

def createTeacher(request):
    """Веб-сервис, предоставляющий занесение приглашенного преподавателя в базу"""
    if request.method == 'POST':
        try:
            data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
                    'military_post': request.POST.get('military_post'), 'military_rank': request.POST.get('military_rank'), 'cycle': request.POST.get('cycle'),
                    'role': request.POST.get('role'), 'login': request.POST.get('login'), 'password': request.POST.get('password')}
            validateTeacherData(data)
            addNewTeacherToDatabase(data)
            return JsonResponse({'success': True}) 
        except Exception as e:
            logger.error("The data for teacher creating is not corrected")
            return JsonResponse({'success': False, 'message': e})


def updateTeacher(request, id):
    """Веб-сервис, предоставляющий обновление информации о преподавателе"""
    if request.method == 'POST':
        try:
            data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
                    'military_post': request.POST.get('military_post'), 'military_rank': request.POST.get('military_rank'), 'cycle': request.POST.get('cycle'),
                    'role': request.POST.get('role'), 'login': request.POST.get('login'), 'password': request.POST.get('password')}
            validateTeacherData(data)
            updateExistingTeacher(data, id)
            return JsonResponse({'success': True}) 
        except Exception as e:
            logger.error("The data for teacher updating is not corrected")
            return JsonResponse({'success': False, 'message': e})


def deleteTeacher(request, id):
    """Веб-сервис, предоставляющий увольнение преподавателей с кафедры"""
    if request.method == 'POST':
        try:
            deleteTeacherFromDatabase(id)
            logger.info(f'teacher with id {id} was removed succesfully')
            return JsonResponse({'success': True}) 
        except Exception as e:
            logger.error(f'Failed to remove teacher with id {id}')
            return JsonResponse({'success': False, 'message': e})



# API для взвода
def getPlatoonByStudent(request, id):
    """Получить объект взвода, в котором находится студент с номером id"""
    platoon = Student.objects.get(id=id).platoon_number;
    if not platoon:
        logger.error(f"platoon for student with id {id} doesn't exist")
        return JsonResponse({"platoon": None})
    else:
        logger.info(f"get correct platoon for student with id {id}")
        return JsonResponse(platoon, safe=False, encoder=PlatoonEncoder)


def getStudentsByPlatoon(request, id):
    """ Получить список студентов по номеру взвода, который представлен id """
    try:
        platoon = getPlatoonByNumber(id)
        students = platoon.student_set.all()
        logger.info(f'get students from platoon with platoon number {id}')
        return JsonResponse({'students': students}, safe=False, encoder=StudentEncoder)
    except Exception as e:
        logger.error(f'platoon with platoon_number {id} does not exist')
        return JsonResponse({'platoon': None, 'message': e})


def getPlatoonTutor(request, id):
    """Получение куратора взвода с номером id"""
    try:
        platoon = getPlatoonByNumber(id)

        tutor = platoon.tutor
        if not tutor:
            logger.error(f'platoon with platoon_number {id} does not have a tutor')
            return JsonResponse({'tutor': None, 'message': 'У данного взвода нет куратора'})
        logger.info(f'get tutor of platoon with platoon number {id}')
        return JsonResponse({'tutor': tutor}, safe=False, encoder=TeacherEncoder)
    except Exception as e:
        logger.error(f'platoon with platoon_number {id} does not exist')
        return JsonResponse({'platoon': None, 'message': e})


def createPlatoon(request):
    """Добавление нового взвода на кафедру"""
    if request.method == 'POST':
        data = {'platoon_number': request.POST.get('platoon_number'), 'tutor': request.POST.get('tutor'), 'year': request.POST.get('year'),
                'status': request.POST.get('status')}
        try:
            result = validateDataForPlatoon(data)
            addNewPlatoon(result) 
            platoon_number = request.POST.get('platoon_number')
            logger.info(f'create a new platoon with platoon number {platoon_number}')
            return JsonResponse({'success': True}) 
        except Exception as e:
            logger.error("The data for platoon creating is not corrected")
            return JsonResponse({'success': False, 'message': e})


def updatePlatoon(request, id):
    """Обновление данных существующего взвода на кафедре"""
    if request.method == 'POST':
        data = {'platoon_number': request.POST.get('platoon_number'), 'tutor': request.POST.get('tutor'), 'year': request.POST.get('year'),
                'status': request.POST.get('status')}
        try:
            result = validateDataForPlatoon(data)
            updatePlatoon(result, id)
            logger.info(f'update a platoon with platoon number {id}')
            return JsonResponse({'success': True}) 
        except Exception as e:
            logger.error("The data for platoon updating is not corrected")
            return JsonResponse({'success': False, 'message': e})


def deletePlatoon(request, id):
    """ 'Выпуск' взвода с кафедры """
    if request.method == 'POST':
        try:
            deletePlatoonWithGraduation(id)
            logger.info(f'delete a platoon with platoon number {id}')
            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f"Failed to delete the platoon with number {id}")
            return JsonResponse({'success': False, 'message': e})

























# TODO: вынести в бизнес-логику журнала
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




