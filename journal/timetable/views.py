import logging

from rest_framework import viewsets
from users.models import *
from .timetable_service import *
from .serializers import SubjectSerializer, SubjectClassSerializer


logger = logging.getLogger(__name__)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectClassViewSet(viewsets.ModelViewSet):
    queryset = SubjectClass.objects.all()
    serializer_class = SubjectClassSerializer
