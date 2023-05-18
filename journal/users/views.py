import logging
from django.core.serializers import serialize

from django.core.serializers.json import json
from marks.marks_services import get_ceils_by_platoon_and_subject, get_ceils_for_student
from marks.serializers import CeilSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from .platoon_services import delete_platoon, get_platoon_by_number, get_students_by_platoon
from .teacher_services import add_new_teacher_to_db, get_teacher, update_existing_teacher, delete_teacher
from .student_services import get_student, add_new_student_to_db, update_existing_student, delete_student
from .models import *
from .serializers import StudentProfileSerializer, TeacherProfileSerializer, PlatoonSerializer, UserSerializer
from timetable.serializers import *
from timetable.timetable_service import get_all_days_in_this_month, get_classes_by_platoon_and_subject, get_platoon_timetable, get_subject, get_subject_for_student, get_timetable_for_teacher


logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    

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
            user = User.objects.get(id=body_data['user'])
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

    @action(methods=['get'], detail=False)
    def student_profile(self, request):
        user = self.request.user
        serializer = StudentProfileSerializer(user.studentprofile)
        return Response(serializer.data)

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
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return TeacherProfile.objects.filter(status='работает')

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
            user = User.objects.get(id=body_data['user'])
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

    @action(methods=['get'], detail=False)
    def logins(self, request):
        logins = User.objects.all()
        serializer = UserSerializer(logins, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def teacher_profile(self, request):
        user = self.request.user
        print(user)
        serializer = TeacherProfileSerializer(user.teacherprofile)
        return Response(serializer.data)


    @action(methods=['get'], detail=True)
    def subjects(self, request, pk):
        logger.info('GET: get subject list for teacher')
        teacher = get_teacher(pk)
        subjects = teacher.subject_set.all()
        logger.info(f'get subjects for teacher with id {pk}')
        return Response(SubjectSerializer(subjects, many=True).data)

    @action(methods=['get'], detail=True)
    def timetable(self, request, pk):
        logger.info('GET: get timetable list for teacher')
        teacher = get_teacher(pk)
        result = get_timetable_for_teacher(teacher)
        return Response(result)


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
        students = get_students_by_platoon(pk)
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def tutor(self, request, pk):
        logger.info('GET: get tutor for platoon')
        platoon = get_platoon_by_number(pk)
        serializer = TeacherProfileSerializer(platoon.tutor)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def commander(self, request, pk):
        logger.info('GET: get commander for platoon')
        commander = get_students_by_platoon(pk).get(military_post='командир взвода')
        serializer = StudentProfileSerializer(commander)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def count(self, request, pk):
        logger.info('GET: get count for platoon')
        count = len(get_students_by_platoon(pk))
        return Response({'count': count})

    @action(methods=['get'], detail=True)
    def timetable(self, request, pk):
        logger.info('GET: get timetable for platoon')
        platoon = get_platoon_by_number(pk)
        month_days = get_all_days_in_this_month(platoon.study_day)
        all_timetable = list()
        for day in month_days:
            timetable = get_platoon_timetable(pk, day)
            all_timetable.append(timetable)
        return Response(all_timetable)

    @action(methods=['get'], detail=True)
    def classes(self, request, pk):
        platoon = get_platoon_by_number(pk)
        subject = get_subject(request.GET.get('subj_id'))
        classes = get_classes_by_platoon_and_subject(platoon, subject)
        serializer = SubjectClassSerializer(classes, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def journal(self, request, pk):
        """ В заголовках необходимо добавить subj_id в качестве id предмета """
        logger.info('GET: get marks for platoon by subject')
        subj_id = request.GET.get('subj_id')
        ceils = get_ceils_by_platoon_and_subject(subj_id, pk)
        return Response(ceils)
