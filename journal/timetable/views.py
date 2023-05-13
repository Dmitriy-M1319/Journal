import logging
from django.core.serializers.json import json

from rest_framework import viewsets
from rest_framework.response import Response
from users.teacher_services import get_teacher
from timetable.models import CourseDirection, DirectionsSubjects
from users.models import *
from .timetable_service import *
from .serializers import SubjectSerializer, SubjectClassSerializer
from users.serializers import CourseDirectionSerializer


logger = logging.getLogger(__name__)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def create(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        teacher = get_teacher(body_data['teacher'])
        subject = Subject.objects.create(name=body_data['name'],
                                         teacher=teacher,
                                         hours_count=body_data['hours_count'],
                                         form=body_data['form'])
        direction = CourseDirection.objects.get(id=body_data['direction'])
        DirectionsSubjects.objects.create(course_direction=direction, subject=subject)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)


class SubjectClassViewSet(viewsets.ModelViewSet):
    queryset = SubjectClass.objects.all()
    serializer_class = SubjectClassSerializer


class CourseDirectionViewSet(viewsets.ModelViewSet):
    queryset = CourseDirection.objects.all()
    serializer_class = CourseDirectionSerializer
