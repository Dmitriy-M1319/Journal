from django.http import JsonResponse

from users.models import Student
from journal.encoders import *
import logging

logger = logging.getLogger(__name__)


# TODO: вынести в бизнес-логику журнала
def getJournalCeils(request, id):
    """Получить оценки студента по всем предметам"""
    student = Student.objects.get(id=id)
    if not student:
        logger.error(f"student with id {id} doesn't exist")
        return JsonResponse({"journal_ceils": None})
    
    ceils = student.journalceil_set.all()
    logger.info(f'get ceils for student {id}')
    return JsonResponse(ceils, safe=False, encoder=JournalCeilEncoder)



















