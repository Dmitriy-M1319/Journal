import logging

from django.http import JsonResponse
from journal.base_view import baseView
from marks.marks_services import addNewJournalCeil, deleteJournalCeilFromDb, getJournalCeilsBySubject, getJournalCeilsForStudent, updateExistingJournalCeil, validateMarkData

from journal.encoders import *

logger = logging.getLogger(__name__)


@baseView
def getJournalCeilsView(request, id):
    """Получить оценки студента по всем предметам"""
    ceils = getJournalCeilsForStudent(id)
    return JsonResponse(ceils, safe=False, encoder=JournalCeilEncoder)


@baseView
def getCeilsBySubjectView(request, id):
    """Веб-сервис, предоставляющий оценки по определенному предмету"""
    ceils = getJournalCeilsBySubject(id)
    return JsonResponse(ceils, safe=False, encoder=JournalCeilEncoder)


def _getValidatedJournalCeilData(request):
    data = {'student': request.POST.get('student'), 'subject_class': request.POST.get('subject_class'),
            'mark': request.POST.get('mark'), 'attendance': request.POST.get('attendance')}
    return validateMarkData(data)


@baseView
def createCeilView(request):
    """Веб-сервис, предоставляющий создание новой оценки"""
    if request.method == 'POST':
        addNewJournalCeil(_getValidatedJournalCeilData(request))
        return JsonResponse({'success': True})


@baseView
def updateCeilView(request, id):
    """Веб-сервис, предоставляющий обновление существующей оценки"""
    if request.method == 'POST':
        updateExistingJournalCeil(_getValidatedJournalCeilData(request), id)
        return JsonResponse({'success': True})


def deleteCeilView(request, id):
    """Веб-сервис, предоставляющий удаление существующей оценки"""
    if request.method == 'POST':
        deleteJournalCeilFromDb(id)
        return JsonResponse({'success': True})

