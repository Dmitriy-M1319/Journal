from rest_framework import serializers

from .models import CourseDirection, StudentProfile, TeacherProfile, User, Platoon


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')


class StudentCreateSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    surname = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    birth_year = serializers.IntegerField()
    patronymic = serializers.CharField(max_length=40)
    military_post = serializers.CharField(max_length=255)
    platoon = serializers.IntegerField()
    department = serializers.CharField(max_length=255, required=False)
    group_number = serializers.IntegerField(required=False)
    order_of_expulsion = serializers.CharField(required=False, allow_blank=True)
    marital_status = serializers.CharField(max_length=30, required=False)
    address = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=11, required=False)
    public_load = serializers.CharField(max_length=50, required=False)
    sports_category = serializers.CharField(max_length=100, required=False)

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data['user'])
        platoon = Platoon.objects.get(platoon_number=validated_data['platoon'])
        result_data = validated_data
        result_data['user'] = user
        result_data['platoon'] = platoon
        return StudentProfile.objects.create(**result_data)

    def update(self, instance, validated_data):
        user = User.objects.get(pk=validated_data.get('user', 
                                                      instance.user._get_pk_val()))
        platoon = Platoon.objects.get(pk=validated_data.get('platoon', 
                                                      instance.platoon))
        instance.user = user
        instance.surname = validated_data.get('surname', instance.surname)
        instance.name = validated_data.get('name', instance.name)
        instance.birth_year = validated_data.get('birth_year', instance.birth_year)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.military_post = validated_data.get('military_post', instance.military_post)
        instance.platoon = platoon
        instance.department = validated_data.get('department', instance.department)
        instance.group_number = validated_data.get('group_number', instance.group_number)
        instance.order_of_expulsion = validated_data.get('order_of_expulsion', instance.order_of_expulsion)
        instance.marital_status = validated_data.get('marital_status', instance.marital_status)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.public_load = validated_data.get('public_load', instance.public_load)
        instance.sports_category = validated_data.get('sports_category', instance.sports_category)
        instance.save()
        return instance
    
    def validate_military_post(self, value):
        _military_posts = ['студент', 'командир взвода']
        if value not in _military_posts:
            raise serializers.ValidationError("Некорректная воинская должность")
        return value


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('__all__')


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

