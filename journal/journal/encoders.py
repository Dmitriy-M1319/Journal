"""Модуль, который будет представлять Json энкодеры для всех моделей базы данных"""
from users.models import Platoon, Student, Teacher
from timetable.models import Subject, SubjectClass
from marks.models import JournalCeil
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize


class TeacherEncoder(DjangoJSONEncoder):
    """Encoder для модели Teacher"""
    def default(self, obj):
        if isinstance(obj, Teacher):
            return {'surname': obj.surname, 
                    'name': obj.name,
                    'patronymic': obj.patronymic,
                    'military_rank': obj.teacherprofile.military_rank,
                    'military_post': obj.military_post,
                    'cycle': obj.teacherprofile.cycle,
                    'login': obj.username,
                    'status': obj.teacherprofile.status
                    }
        return super().default(obj)


class PlatoonEncoder(DjangoJSONEncoder):
    """Encoder для модели Platoon"""
    def default(self, obj):
        if isinstance(obj, Platoon):
            return {
                    'number': obj.platoon_number,
                    'year': obj.year,
                    'tutor': obj.tutor.json()
                    }
        return super().default(obj)


class StudentEncoder(DjangoJSONEncoder):
    """Encoder для модели Student"""
    def default(self, obj):
        if isinstance(obj, Student):
            return {
                    'surname': obj.surname, 
                    'name': obj.name,
                    'patronymic': obj.patronymic,
                    'sex': obj.studentprofile.sex,
                    'platoon': obj.studentprofile.platoon.json(),
                    'military_post': obj.military_post,
                    'login': obj.username,
                    'department': obj.studentprofile.department,
                    'group_number': obj.studentprofile.group_number,
                    'status': obj.studentprofile.active
                    }
        return super().default(obj)


class SubjectEncoder(DjangoJSONEncoder):    
    """Encoder для модели Subject"""
    def default(self, obj):
        if isinstance(obj, Subject):
            return {
                    'teacher': obj.teacher.json(),
                    'name': obj.name,
                    'hours_count': obj.hours_count,
                    'form': obj.form
                    }
        return super().default(obj)


class SubjectClassEncoder(DjangoJSONEncoder):
    """Encoder для модели SubjectClass"""
    def default(self, obj):
        if isinstance(obj, SubjectClass):
            return {
                    'subject': obj.subject.json(),
                    'platoon': obj.platoon.json(),
                    'date': obj.class_date,
                    'theme_number': obj.theme_number,
                    'theme_name': obj.theme_name,
                    'class_number': obj.class_number,
                    'class_name': obj.class_name,
                    'class_type': obj.class_type,
                    'classroom': obj.classroom
                    }
        return super().default(obj)


class JournalCeilEncoder(DjangoJSONEncoder):
    """Encoder для модели JournalCeil"""
    def default(self, obj):
        if isinstance(obj, JournalCeil):
            return {
                    'student': obj.student.json(),
                    'subject_class': obj.subject_class.json(),
                    'mark': obj.mark,
                    'attendance': obj.attendance
                    }
        return super().default(obj)
