import logging

from django.core.serializers.json import json
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .platoon_services import get_platoon_by_number
from .teacher_services import add_new_teacher_to_db, update_existing_teacher, delete_teacher
from .student_services import get_student, add_new_student_to_db, update_existing_student, delete_student
from .models import *
from .serializers import StudentProfileSerializer, TeacherProfileSerializer, PlatoonSerializer


logger = logging.getLogger(__name__)

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def create(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user = User.objects.get(id=body_data['user_id'])
            profile = add_new_student_to_db(user, body_data)
            return Response(StudentProfileSerializer(profile).data)
        except Exception as e:
            return Response({'message': e}, status=500)

    def update(self, request, pk=None):
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user = User.objects.get(id=body_data['user_id'])
            profile = update_existing_student(user, body_data, pk)
            return Response(StudentProfileSerializer(profile).data)
        except Exception as e:
            return Response({'message': e}, status=500)

    def destroy(self, request, pk=None):
        try:
            delete_student(pk)
            return Response(status=201)
        except Exception as e:
            return Response({'message': e}, status=500)

    @action(methods=['get'], detail=True)
    def platoon(self, request, id):
        try:
            student = get_student(id)
            serializer = PlatoonSerializer(student.platoon)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': e}, status=500)


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    def create(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user = User.objects.get(id=body_data['user_id'])
            profile = add_new_teacher_to_db(user, body_data)
            return Response(TeacherProfileSerializer(profile).data)
        except Exception as e:
            return Response({'message': e}, status=500)

    def update(self, request, pk=None):
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user = User.objects.get(id=body_data['user_id'])
            profile = update_existing_teacher(user, body_data, pk)
            return Response(TeacherProfileSerializer(profile).data)
        except Exception as e:
            return Response({'message': e}, status=500)

    def destroy(self, request, pk=None):
        try:
            delete_teacher(pk)
            return Response(status=201)
        except Exception as e:
            return Response({'message': e}, status=500)


class PlatoonViewSet(viewsets.ModelViewSet):
    queryset = Platoon.objects.all()
    serializer_class = PlatoonSerializer
    
    @action(methods=['get'], detail=True)
    def students(self, request, id):
        platoon = get_platoon_by_number(id)
        students = StudentProfile.objects.filter(platoon=platoon)
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def tutor(self, request, id):
        platoon = get_platoon_by_number(id)
        serializer = TeacherProfileSerializer(platoon.tutor)
        return Response(serializer.data)
