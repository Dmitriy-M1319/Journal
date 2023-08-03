from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Subject, SubjectClass, CourseDirection
from users.services.teacher import get_teacher


class SubjectCreateSerializer(serializers.Serializer):
    teacher = serializers.IntegerField()
    name = serializers.CharField()
    hours_count = serializers.IntegerField()
    form = serializers.CharField()

    def create(self, validated_data):
        teacher = get_teacher(validated_data['teacher'])
        result = validated_data
        result['teacher'] = teacher
        return Subject(**result)

    def update(self, instance, validated_data):
        teacher = get_teacher(validated_data.get('teacher', instance.teacher))
        instance.teacher = teacher
        instance.name = validated_data.get('name', instance.name)
        instance.hours_count = validated_data.get('hours_count', instance.hours_count)
        instance.form = validated_data.get('form', instance.form)

    def validate_hours_count(self, value):
        if value <= 0:
            raise ValidationError('Некорректное количество часов для предмета')
        return value

    def validate_form(self, value):
        if value not in ['экзамен', 'зачет']:
            raise ValidationError('Некорректная форма итоговой аттестации')
        return value

    
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('__all__')


class SubjectClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectClass
        fields = ('__all__')


class CourseDirectionCreateSerializer(serializers.Serializer):
    course = serializers.IntegerField()
    direction = serializers.CharField()

    def create(self, validated_data):
        return CourseDirection(**validated_data)

    def update(self, instance, validated_data):
        instance.course = validated_data.get('course', instance.course)
        instance.direction = validated_data.get('direction', instance.diretion)


class CourseDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDirection
        fields = ('__all__')
