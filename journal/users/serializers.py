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


class TeacherCreateSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    surname = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    patronymic = serializers.CharField(max_length=40)
    military_post = serializers.CharField(max_length=255)
    military_rank = serializers.CharField(max_length=20)
    cycle = serializers.CharField(max_length=255)
    teacher_role = serializers.IntegerField()

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data['user'])
        result = validated_data
        result['user'] = user
        return TeacherProfile.objects.create(**result)
 
    def update(self, instance, validated_data):
        user = User.objects.get(pk=validated_data.get('user', 
                                                      instance.user._get_pk_val()))
        instance.user = user
        instance.surname = validated_data.get('surname', instance.surname)
        instance.name = validated_data.get('name', instance.name)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.military_post = validated_data.get('military_post', instance.military_post)
        instance.military_rank = validated_data.get('military_rank', instance.military_rank) 
        instance.teacher_role = validated_data.get('teacher_role', instance.teacher_role) 
        instance.cycle = validated_data.get('cycle', instance.cycle)
        instance.save()
        return instance


    def validate_military_rank(self, value):
        _military_ranks = ['лейтенант', 'старший лейтенант', 'капитан', 'майор', 'подполковник', 'полковник']
        if value not in _military_ranks:
            raise serializers.ValidationError("Некорректное воинское звание")
        return value

    def validate_teacher_role(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("Некорректное значение для роли преподавателя")
        return value

   
class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = '__all__'


class PlatoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platoon
        fields = ('platoon_number', 'tutor', 'year', 'order_of_enrollment', 'course', 'study_day', 'status')


class CourseDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDirection
        fields = ('id', 'course', 'direction')

