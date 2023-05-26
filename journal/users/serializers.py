from rest_framework import serializers
from .models import CourseDirection, StudentProfile, TeacherProfile, User, Platoon


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('id', 
                  'user', 
                  'surname', 
                  'name', 
                  'patronymic', 
                  'platoon', 
                  'military_post', 
                  'birth_year',
                  'department', 
                  'group_number',
                  'order_of_expulsion',
                  'marital_status',
                  'address',
                  'phone_number',
                  'public_load',
                  'sports_category')


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ('id', 'user',  'surname', 'name', 'patronymic', 'military_post', 'teacher_role', 'military_rank', 'cycle')


class PlatoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platoon
        fields = ('platoon_number', 'tutor', 'year', 'order_of_enrollment', 'course', 'study_day', 'status')


class CourseDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDirection
        fields = ('id', 'course', 'direction')
