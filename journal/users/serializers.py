from rest_framework import serializers
from .models import StudentProfile, TeacherProfile, User, Platoon


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('id', 'user', 'patronymic', 'military_post', 'department', 'group_number')


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ('id', 'user', 'patronymic', 'military_post', 'military_rank', 'cycle')


class PlatoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platoon
        fields = ('platoon_number', 'tutor', 'year', 'course', 'status')
