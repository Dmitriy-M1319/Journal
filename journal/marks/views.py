import logging

from django.http import JsonResponse
from django.http.response import json
from rest_framework import viewsets

from marks.marks_services import * 

logger = logging.getLogger(__name__)

class CeilViewSet(viewsets.ModelViewSet):
    queryset = JournalCeil.objects.all()
    serializer_class = CeilSerializer
