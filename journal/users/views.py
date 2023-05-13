import logging

from django.core.serializers.json import json
from marks.marks_services import get_ceils_by_platoon_and_subject, get_ceils_for_student
from marks.serializers import CeilSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .platoon_services import delete_platoon, get_platoon_by_number
from .teacher_services import add_new_teacher_to_db, get_teacher, update_existing_teacher, delete_teacher
from .student_services import get_student, add_new_student_to_db, update_existing_student, delete_student
from .models import *
from .serializers import StudentProfileSerializer, TeacherProfileSerializer, PlatoonSerializer, UserSerializer
from timetable.serializers import *
from timetable.timetable_service import get_platoon_timetable, get_subject, get_subject_for_student


logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True)
    def teacher_profile(self, request, pk):
        """ Получить профиль преподавателя по его id записи авторизации """
        user = User.objects.get(id=pk)
        serializer = TeacherProfileSerializer(user.teacherprofile)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def student_profile(self, request, pk):
        """ Получить профиль студента по его id записи авторизации """
        user = User.objects.get(id=pk)
        serializer = StudentProfileSerializer(user.studentprofile)
        return Response(serializer.data)

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def create(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user = User.objects.get(id=body_data['user'])
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
    def platoon(self, request, pk):
        try:
            student = get_student(pk)
            serializer = PlatoonSerializer(student.platoon)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': e}, status=500)

    @action(methods=['get'], detail=True)
    def marks(self, request, pk):
        """Получить оценки студента по всем предметам"""
        ceils = get_ceils_for_student(pk)
        serializer = CeilSerializer(ceils, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def subjects(self, request, pk):
        subjects = get_subject_for_student(pk)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    def create(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            print(body_data)
            user = User.objects.get(id=body_data['user'])
            profile = add_new_teacher_to_db(user, body_data)
            serializer = TeacherProfileSerializer(profile)
            print(serializer)
            return Response(serializer.data)
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

    @action(methods=['get'], detail=True)
    def subjects(self, request, pk):
        logger.info('GET: get subject list for teacher')
        teacher = get_teacher(pk)
        subjects = teacher.subject_set.all()
        logger.info(f'get subjects for teacher with id {pk}')
        return Response(SubjectSerializer(subjects, many=True).data)

    @action(methods=['get'], detail=True)
    def classes(self, request, pk):
        """ Получить все занятия по предмету с номером subject_id, который ведет преподаватель с идентификатором id """
        logger.info('GET: get subject class list for teacher')
        teacher = get_teacher(pk) 
        subject = get_subject(request.GET.get('subject_id'))
        if not teacher.subject_set.filter(name=subject.name):
            return Response({'subject_classes': None, 'message': 'Данный предмет не ведется преподавателем'}, status=500)
        subject_classes = subject.subjectclass_set.all()
        logger.info(f'get subject classes for teacher with id {pk}')
        serializer = SubjectClassSerializer(subject_classes, many=True)
        return Response(serializer.data)


class PlatoonViewSet(viewsets.ModelViewSet):
    queryset = Platoon.objects.all()
    serializer_class = PlatoonSerializer

    def destroy(self, request, pk=None):
        try:
            delete_platoon(pk)
            return Response(status=201)
        except Exception as e:
            return Response({'message': e}, status=500)

    @action(methods=['get'], detail=True)
    def students(self, request, pk):
        logger.info('GET: get students for platoon')
        platoon = get_platoon_by_number(pk)
        students = StudentProfile.objects.filter(platoon=platoon)
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def tutor(self, request, pk):
        logger.info('GET: get tutor for platoon')
        platoon = get_platoon_by_number(pk)
        serializer = TeacherProfileSerializer(platoon.tutor)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def timetable(self, request, pk):
        """ В заголовках необходимо передать день с ключом day """
        logger.info('GET: get timetable for platoon')
        try:
            timetable = get_platoon_timetable(pk, request.GET.get('day'))
            serializer = SubjectClassSerializer(timetable, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)}, status=404)


    @action(methods=['get'], detail=True)
    def journal(self, request, pk):
        """ В заголовках необходимо добавить subj_id в качестве id предмета """
        logger.info('GET: get marks for platoon by subject')
        subj_id = request.GET.get('subj_id')
        ceils = get_ceils_by_platoon_and_subject(subj_id, pk)
        return Response(ceils)
