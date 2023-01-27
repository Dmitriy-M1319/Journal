from django.http import JsonResponse, HttpResponseRedirect

from .encoders import JournalCeilEncoder, PlatoonEncoder, TeacherEncoder
from .timetable_service import *
from .student_services import *
from .models import *
import hashlib, logging

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
        return JsonResponse(timetable)


def createStudent(request):
    """Добавить студента на кафедру"""
    if request.method == 'POST':
        try:
            validated = validateData(request.POST.get('surname'), request.POST.get('name'), request.POST.get('patronymic'), request.POST.get('sex'),
                                     request.POST.get('platoon'), request.POST.get('military_rank'), request.POST.get('login'), request.POST.get('password'), 
                                     request.POST.get('department'), request.POST.get('group_number'))
            addStudent(validated)
            return JsonResponse({'success': True}) 
        except Exception:
            logger.error("The data for student creating is not corrected")
            return JsonResponse({'success': False, 'message': "The data for student creating is not corrected"})
            

        




     
        


























# Получение всех преподавателей из базы данных
def teacher_index(request):
    teachers = Teacher(surname='Рязанов', 
                       name='Владимир', 
                       patronymic='Анатольевич', 
                       military_rank='полковник', 
                       military_post='начальник кафедры специальной подготовки', 
                       cycle='цикл', 
                       login='ryazanov_v_a', 
                       password='12345678')  
    return JsonResponse(teachers, safe=False, encoder=TeacherEncoder)


# Создание записи преподавателя и сохранение его в базу данных
def teacher_create(request):
    if request.method == 'POST':
        teacher = Teacher()
        teacher.surname = request.POST.get('surname')
        teacher.name = request.POST.get('name')
        teacher.patronymic = request.POST.get('patronymic')
        teacher.military_rank = request.POST.get('military_rank') 
        teacher.military_post = request.POST.get('military_post') 
        teacher.cycle = request.POST.get('cycle') 
        teacher.login = request.POST.get('login') 
        #teacher.password = hashlib.md5(request.POST.get('password').encode()).hexdigest()
        teacher.save()
    return HttpResponseRedirect("/teachers")


