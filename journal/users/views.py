from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from .services.platoon import *
from .services.teacher import * 
from .services.student import *
from utils.serializers import MessageResponseSerializer
from utils.services import *
from marks.marks_services import get_ceils_by_platoon_and_subject, get_ceils_for_student
from marks.serializers import CeilSerializer
from .models import *
from .serializers import StudentProfileSerializer, TeacherProfileSerializer, PlatoonSerializer, UserSerializer
from timetable.serializers import *
from timetable.services import get_classes_by_platoon_and_subject, get_subject, get_subject_classes_for_teacher, get_subject_for_student, get_timetable_for_teacher


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            body_data = load_post_data(request)
            user = User.objects.get(id=body_data['user'])
            profile = add_new_student_to_db(user, body_data)
            return Response(StudentProfileSerializer(profile).data)
        except Exception as e:
            return Response({'message': e}, status=500)

    def update(self, request, pk=None):
        try:
            body_data = load_post_data(request)
            user = User.objects.get(id=body_data['user'])
            profile = update_existing_student(user, body_data, pk)
            return Response(StudentProfileSerializer(profile).data)
        except Exception as e:
            return Response({'message': e}, status=500)
 
    @action(methods=['post'], detail=True)
    def expulse(self, request, pk=None):
        try:
            expulse_student(pk)
            return Response(MessageResponseSerializer({'success': True, 'message': 'Успешно'}).data)
        except Exception as e:
            return Response(MessageResponseSerializer({'success': False, 'message': e}).data, status=500)

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
            return Response(MessageResponseSerializer({'success': False, 'message': e}).data, status=500)

    @action(methods=['get'], detail=True)
    def marks(self, request, pk):
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
            body_data = load_post_data(request)
            user = User.objects.get(id=body_data['user'])
            profile = add_new_teacher_to_db(user, body_data)
            serializer = TeacherProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response(MessageResponseSerializer({'success': False, 'message': e}).data, status=500)

    def update(self, request, pk=None):
        try:
            body_data = load_post_data(request)
            user = User.objects.get(id=body_data['user'])
            profile = update_existing_teacher(user, body_data, pk)
            return Response(TeacherProfileSerializer(profile).data)
        except Exception as e:
            return Response(MessageResponseSerializer({'success': False, 'message': e}).data, status=500)

    @action(methods=['post'], detail=True)
    def dismiss(self, request, pk=None):
        try:
            dismiss_teacher(pk)
            return Response(MessageResponseSerializer({'success': True, 'message': 'Успешно'}).data)
        except Exception as e:
            return Response(MessageResponseSerializer({'success': False, 'message': e}).data, status=500)

    @action(methods=['get'], detail=False)
    def logins(self, request):
        logins = User.objects.all()
        serializer = UserSerializer(logins, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def teacher_profile(self, request):
        user = self.request.user
        serializer = TeacherProfileSerializer(user.teacherprofile)
        return Response(serializer.data)


    @action(methods=['get'], detail=True)
    def subjects(self, request, pk):
        teacher = get_teacher(pk)
        subjects = teacher.subject_set.all()
        return Response(SubjectSerializer(subjects, many=True).data)

    @action(methods=['get'], detail=True)
    def timetable(self, request, pk):
        teacher = get_teacher(pk)
        result = get_timetable_for_teacher(teacher)
        return Response(result)


    @action(methods=['get'], detail=True)
    def classes(self, request, pk):
        """ Получить все занятия по предмету с номером subject_id, который ведет преподаватель с идентификатором id """
        try:
            teacher = get_teacher(pk)
            subject_classes = get_subject_classes_for_teacher(teacher, request.GET.get('subject_id'))
            serializer = SubjectClassSerializer(subject_classes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(MessageResponseSerializer({'success': False, 'message': e}).data, status=500)


class PlatoonViewSet(viewsets.ModelViewSet):
    queryset = Platoon.objects.all()
    serializer_class = PlatoonSerializer
    permission_classes = (permissions.IsAuthenticated,)


    @action(methods=['get'], detail=True)
    def students(self, request, pk):
        students = get_students_by_platoon(pk)
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def tutor(self, request, pk):
        platoon = get_platoon_by_number(pk)
        serializer = TeacherProfileSerializer(platoon.tutor)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def commander(self, request, pk):
        commander = get_students_by_platoon(pk).get(military_post='командир взвода')
        serializer = StudentProfileSerializer(commander)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def count(self, request, pk):
        count = len(get_students_by_platoon(pk))
        return Response({'count': count})

    @action(methods=['get'], detail=True)
    def timetable(self, request, pk):
        timetable = create_timetable_for_platoon(pk) 
        return Response(timetable)

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
        subj_id = request.GET.get('subj_id')
        ceils = get_ceils_by_platoon_and_subject(subj_id, pk)
        return Response(ceils)
