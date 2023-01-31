from django.http import JsonResponse, HttpResponseRedirect

from .encoders import *
from .timetable_service import *
from .student_services import *
from .models import *
import logging

logger = logging.getLogger(__name__)

# API for Student
def getPlatoon(request, id):
    """Получить объект взвода, в котором находится студент"""
    platoon = Student.objects.get(id=id).platoon_number;
    if not platoon:
        logger.error(f"platoon for student with id {id} doesn't exist")
        return JsonResponse({"platoon": None})
    else:
        logger.info(f"get correct platoon for student with id {id}")
        return JsonResponse(platoon, safe=False, encoder=PlatoonEncoder)


def getJournalCeils(request, id):
    """Получить оценки студента по всем предметам"""
    student = Student.objects.get(id=id)
    if not student:
        logger.error(f"student with id {id} doesn't exist")
        return JsonResponse({"journal_ceils": None})
    
    ceils = student.journalceil_set.all()
    logger.info(f'get ceils for student {id}')
    return JsonResponse(ceils, safe=False, encoder=JournalCeilEncoder)


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


def createStudent(request):
    """Добавить студента на кафедру"""
    if request.method == 'POST':
        try:
            data = {'surname': request.POST.get('surname'), 'name': request.POST.get('name'), 'patronymic': request.POST.get('patronymic'),
                    'sex': request.POST.get('sex'), 'military_post': request.POST.get('military_post'), 'platoon': request.POST.get('platoon'),
                    'login': request.POST.get('login'), 'password': request.POST.get('password'), 'department': request.POST.get('department'),
                    'group_number': request.POST.get('group_number')}
            addStudent(data)
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


# API для преподавателей (без прав особого пользователя)

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


def getStudentsByPlatoon(request, id):
    """ Получить список студентов по номеру взвода, который представлен id """
    platoon = Platoon.objects.get(platoon_number=id)
    if not platoon:
        logger.error(f'platoon with platoon_number {id} does not exist')
        return JsonResponse({'platoon': None, 'message': 'Взвода с таким номером не существует в базе'})

    students = platoon.student_set.all()
    logger.info(f'get students from platoon with platoon number {id}')
    return JsonResponse({'students': students}, safe=False, encoder=StudentEncoder)


def createTeacher(request):
    """ Добавить нового преподавателя """
    if request.method == 'POST':






















