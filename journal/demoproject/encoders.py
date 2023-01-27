"""Модуль, который будет представлять Json энкодеры для всех моделей базы данных"""
from .models import *
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize


class TeacherEncoder(DjangoJSONEncoder):
    """Encoder для модели Teacher"""
    def default(self, obj):
        if isinstance(obj, Teacher):
            return {'surname': obj.surname, 
                    'name': obj.name,
                    'patronymic': obj.patronymic,
                    'military_rank': obj.military_rank,
                    'military_post': obj.military_post,
                    'cycle': obj.cycle,
                    'login': obj.cycle,
                    'password': obj.password,
                    'status': obj.status
                    }
        return super().default(obj)


class PlatoonEncoder(DjangoJSONEncoder):
    """Encoder для модели Platoon"""
    def default(self, obj):
        if isinstance(obj, Platoon):
            return {
                    'number': obj.platoon_number,
                    'year': obj.year,
                    'tutor': serialize('json', obj.tutor, cls=TeacherEncoder)
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
                    'sex': obj.sex,
                    'platoon': serialize('json', obj.platoon, cls=PlatoonEncoder),
                    'military_post': obj.military_post,
                    'login': obj.login,
                    'password': obj.password,
                    'department': obj.department,
                    'group_number': obj.group_number,
                    'status': obj.active
                    }
        return super().default(obj)


class SubjectEncoder(DjangoJSONEncoder):    
    """Encoder для модели Subject"""
    def default(self, obj):
        if isinstance(obj, Subject):
            return {
                    'teacher': serialize('json', obj.teacher, cls=TeacherEncoder),
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
                    'subject': serialize('json', obj.subject, cls=SubjectEncoder),
                    'platoon': serialize('json', obj.platoon, cls=PlatoonEncoder),
                    'date': obj.date,
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
                    'student': serialize('json', obj.student, cls=StudentEncoder),
                    'subject_class': serialize('json', obj.subject_class, cls=SubjectClassEncoder),
                    'mark': obj.mark,
                    'attendance': obj.attendance
                    }
        return super().default(obj)
