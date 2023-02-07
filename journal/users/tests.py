from django.core.exceptions import ValidationError
from django.test import TestCase

from users.teacher_services import addNewTeacherToDatabase, deleteTeacherFromDatabase, getTeacher, updateExistingTeacher, validateTeacherData

from .models import Teacher

class TeacherServicesTests(TestCase):
    def setUp(self) -> None:
       Teacher.objects.create(surname='Иванов', name='Иван',
                              patronymic='Иванович', military_rank='капитан',
                              military_post='преподаватель', cycle='Цикл 1',
                              role=1, login='ivanov_i_i', password='t12345678',
                              status=True)
       self.input_data_correct = {'surname': 'Сидоров', 'name': 'Петр', 'patronymic': 'Сергеевич',
                    'military_post': 'старший преподаватель', 'military_rank': 'подполковник', 'cycle': 'Цикл 2',
                    'role': 1, 'login': 'sidorov_p_s', 'password': 'oiu564123'}
       self.input_data_incorrect = {'surname': 'Сидоров', 'name': 'Петр', 'patronymic': 'Сергеевич',
                    'military_post': 'csdsdv', 'military_rank': 'ddsfsdfa', 'cycle': 'Цикл 2',
                    'role': 1, 'login': 'sidorov_p_s', 'password': 'oiu564123'}
       self.input_data_updating = {'surname': 'Иванов', 'name': 'Иван', 'patronymic': 'Иванович',
                    'military_post': 'преподаватель', 'military_rank': 'майор', 'cycle': 'Цикл 2',
                    'role': 1, 'login': 'ivanov_i_i', 'password': 't12345678'}


    def test_validated_data(self):
        validated_data1 = validateTeacherData(self.input_data_correct)
        self.assertEqual(validated_data1, self.input_data_correct)
        with self.assertRaises(ValidationError):
            validated_data2 = validateTeacherData(self.input_data_incorrect)


    def test_insert_teacher(self):
        validated_data = validateTeacherData(self.input_data_correct)
        addNewTeacherToDatabase(validated_data)
        teacher = Teacher.objects.get(surname='Сидоров')
        self.assertIsNotNone(teacher)


    def test_update_teacher(self):
        teacher = getTeacher(1)
        self.assertIsNotNone(teacher)
        self.assertEqual(teacher.military_rank, 'капитан')
        validated_data = validateTeacherData(self.input_data_updating)
        updateExistingTeacher(validated_data, 1)
        teacher = getTeacher(1)
        self.assertIsNotNone(teacher)
        self.assertEqual(teacher.military_rank, 'майор')


    def test_delete_teacher(self):
        teacher = getTeacher(1)
        self.assertIsNotNone(teacher)
        deleteTeacherFromDatabase(1)
        teacher = getTeacher(1)
        self.assertFalse(teacher.status)





