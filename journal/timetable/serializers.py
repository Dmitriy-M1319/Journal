from rest_framework import serializers
from .models import Subject, SubjectClass, CourseDirection

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'teacher', 'hours_count', 'form')


class SubjectClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectClass
        fields = ('id', 'subject', 'platoon', 'class_date', 'theme_number', 'theme_name', 'class_number', 'class_name', 'class_type', 'classroom')
