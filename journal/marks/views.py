from django.http import JsonResponse

from users.models import Student
from journal.encoders import *
import logging

logger = logging.getLogger(__name__)


def getJournalCeils(request, id):
    """Получить оценки студента по всем предметам"""
    try:
        student = Student.objects.get(id=id)
        ceils = student.journalceil_set.all()
        logger.info(f'get ceils for student {id}')
        return JsonResponse(ceils, safe=False, encoder=JournalCeilEncoder)
    except Exception as e:
        logger.error(f"student with id {id} doesn't exist")
        return JsonResponse({"journal_ceils": None, 'message': e})


def getCeilsBySubject(request, id):

