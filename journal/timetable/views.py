from rest_framework import viewsets
from rest_framework.response import Response

from timetable.models import CourseDirection, Subject, SubjectClass
from users.models import *
from .services import create_subject
from .serializers import SubjectSerializer, SubjectClassSerializer
from users.serializers import CourseDirectionSerializer
from utils.services import *


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def create(self, request, *args, **kwargs):
        body_data = load_post_data(request)
        subject = create_subject(body_data)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)


class SubjectClassViewSet(viewsets.ModelViewSet):
    queryset = SubjectClass.objects.all()
    serializer_class = SubjectClassSerializer


class CourseDirectionViewSet(viewsets.ModelViewSet):
    queryset = CourseDirection.objects.all()
    serializer_class = CourseDirectionSerializer
