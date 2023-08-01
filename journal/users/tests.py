from django.test import TestCase


from .models import *
from .serializers import *
from .services.teacher import *


class TeacherProfileModelTests(TestCase):
    def test_create_new_teacher_instanse(self):
        user_data = User(username="user1", password="Qwer12345")
        user_data.save()
        user_id = user_data._get_pk_val()
        data = { 
                "user": user_id, 
                "surname": "Иванов",
                "name": "Иван",
                "patronymic": "Иванович",
                "military_post": "преподаватель",
                "teacher_role": 0,
                "military_rank": "капитан",
                "cycle": "цикл информационных систем"
                }
        teacher = add_new_teacher_to_db(TeacherCreateSerializer(data=data))
        data['status'] = 'работает'
        del data["user"]
        data['user_id'] = user_id
        self.assertIsNotNone(teacher)
        self.assertDictContainsSubset(data, teacher.__dict__)

    def test_update_teacher_instanse(self):
        user_data = User(username="user1", password="Qwer12345")
        user_data.save()
        user_id = user_data._get_pk_val()
        data = { 
                "user": user_id, 
                "surname": "Иванов",
                "name": "Иван",
                "patronymic": "Иванович",
                "military_post": "преподаватель",
                "teacher_role": 0,
                "military_rank": "капитан",
                "cycle": "цикл информационных систем"
                }
        teacher = add_new_teacher_to_db(TeacherCreateSerializer(data=data))
        self.assertIsNotNone(teacher)

        data["name"] = 'Петр'
        new_teacher = update_existing_teacher(data, teacher.id)
        self.assertIsNotNone(new_teacher)
        self.assertEqual(new_teacher.name, 'Петр')

    def test_dismiss_teacher_instanse(self):
        user_data = User(username="user1", password="Qwer12345")
        user_data.save()
        user_id = user_data._get_pk_val()
        data = { 
                "user": user_id, 
                "surname": "Иванов",
                "name": "Иван",
                "patronymic": "Иванович",
                "military_post": "преподаватель",
                "teacher_role": 0,
                "military_rank": "капитан",
                "cycle": "цикл информационных систем"
                }
        teacher = add_new_teacher_to_db(TeacherCreateSerializer(data=data))
        self.assertIsNotNone(teacher)

        dismiss_teacher(teacher.id)
        teacher_dismissed = TeacherProfile.objects.get(pk=teacher.id)
        self.assertIsNotNone(teacher_dismissed)
        self.assertEqual(teacher_dismissed.status, 'уволен')

