from django.core.exceptions import ValidationError
from django.test import TestCase
from users.platoon_services import *
from users.teacher_services import *
from users.student_services import *

from .models import *

class TeacherServicesTests(TestCase):
    def setUp(self) -> None:
       teacher = Teacher.objects.create(surname='Иванов', name='Иван',
                              patronymic='Иванович', military_post='преподаватель', username='ivanov_i_i', password='t12345678')
       teacher.teacherprofile.military_rank = 'капитан'
       teacher.teacherprofile.cycle = 'Цикл 1'
       teacher.teacherprofile.teacher_role = 1
       teacher.teacherprofile.status = 'работает'
       teacher.teacherprofile.save()
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
        validated_data1 = validate_teacher_data(self.input_data_correct)
        self.assertEqual(validated_data1, self.input_data_correct)
        with self.assertRaises(ValidationError):
            validated_data2 = validate_teacher_data(self.input_data_incorrect)


    def test_insert_teacher(self):
        validated_data = validate_teacher_data(self.input_data_correct)
        add_new_teacher_to_db(validated_data)
        teacher = Teacher.objects.get(surname='Сидоров')
        self.assertIsNotNone(teacher)


    def test_update_teacher(self):
        teacher = get_teacher(1)
        self.assertIsNotNone(teacher)
        self.assertEqual(teacher.teacherprofile.military_rank, 'капитан')
        validated_data = validate_teacher_data(self.input_data_updating)
        update_existing_teacher(validated_data, 1)
        teacher = get_teacher(1)
        self.assertIsNotNone(teacher)
        self.assertEqual(teacher.teacherprofile.military_rank, 'майор')


    def test_delete_teacher(self):
        teacher = get_teacher(1)
        self.assertIsNotNone(teacher)
        delete_teacher(1)
        with self.assertRaises(Exception):
            teacher = get_teacher(1)



class PlatoonServicesTests(TestCase):
    def setUp(self) -> None:
        teacher = Teacher.objects.create(surname='Иванов', name='Иван',
                              patronymic='Иванович', military_post='преподаватель', username='ivanov_i_i', password='t12345678')
        teacher.teacherprofile.military_rank = 'капитан'
        teacher.teacherprofile.cycle = 'Цикл 1'
        teacher.teacherprofile.teacher_role = 1
        teacher.teacherprofile.status = 'работает'
        teacher.teacherprofile.save()
        self.teacher = teacher
        self.input_data_correct = {'platoon_number': '551', 'tutor': self.teacher.id, 'year': 2021, 'status': 'выпустился'}
        self.input_data_incorrect1 = {'platoon_number': '551', 'tutor': self.teacher.id, 'year': 2021, 'status': 'отчислен'}
        self.input_data_incorrect2 = {'platoon_number': '551', 'tutor': Teacher().id, 'year': 2021, 'status': 'выпустился'}


    def test_validated_data(self):
        validated_data1 = validate_platoon_data(self.input_data_correct) 
        self.assertEqual(validated_data1, self.input_data_correct)
        with self.assertRaises(ValidationError):
            validated_data2 = validate_platoon_data(self.input_data_incorrect1) 
        with self.assertRaises(ValidationError):
            validated_data3 = validate_platoon_data(self.input_data_incorrect2) 


    def test_insert_platoon(self):
        validated_data = validate_platoon_data(self.input_data_correct)
        add_new_platoon_to_db(validated_data)
        platoon = get_platoon_by_number(551)
        self.assertEqual(self.teacher, platoon.tutor)


    def test_update_platoon(self):
        Platoon.objects.create(platoon_number=451, tutor=self.teacher, year=2020, status='учится')
        self.input_data_correct = {'platoon_number': '451', 'tutor': self.teacher.id, 'year': 2021, 'status': 'выпустился'}
        platoon = get_platoon_by_number(451)
        self.assertIsNotNone(platoon)
        self.assertEqual(platoon.platoon_number, 451)
        self.assertEqual(platoon.year, 2020)
        self.assertEqual(platoon.status, 'учится')
        validated_data = validate_platoon_data(self.input_data_correct)
        update_existing_platoon(validated_data, platoon.platoon_number)
        platoon = get_platoon_by_number(451)
        self.assertIsNotNone(platoon)
        self.assertEqual(platoon.platoon_number, 451)
        self.assertEqual(platoon.year, 2021)


    def test_delete_platoon(self):
        Platoon.objects.create(platoon_number=451, tutor=self.teacher, year=2020, status='учится')
        platoon = get_platoon_by_number(451)
        self.assertIsNotNone(platoon)
        delete_platoon(platoon.platoon_number)
        platoon = get_platoon_by_number(451)
        self.assertEqual(platoon.status, 'выпустился')


class StudentServicesTests(TestCase):
    def setUp(self) -> None:
        teacher = Teacher.objects.create(surname='Иванов', name='Иван',
                              patronymic='Иванович', military_post='преподаватель', username='ivanov_i_i', password='t12345678')
        teacher.teacherprofile.military_rank = 'капитан'
        teacher.teacherprofile.cycle = 'Цикл 1'
        teacher.teacherprofile.teacher_role = 1
        teacher.teacherprofile.status = 'работает'
        teacher.teacherprofile.save()
        self.teacher = teacher
        Platoon.objects.create(platoon_number=451, tutor=self.teacher, year=2020, status='учится')

        self.platoon = get_platoon_by_number(451)
        self.input_data_correct = {'surname': 'Сидоров', 'name': 'Петр', 'patronymic': 'Сергеевич', 'sex': 'мужской',
                    'platoon': '451', 'military_post': 'студент', 'login': 'sidorov_p_s', 'password': 'oiu564123',
                    'department': 'FKN', 'group_number': '5'}
        self.input_data_incorrect = {'surname': 'Сидоров', 'name': 'Петр', 'patronymic': 'Сергеевич', 'sex': 'мужской',
                    'platoon': '451', 'military_post': 'заместитель ком.взвода', 'login': 'sidorov_p_s', 'password': 'oiu564123',
                    'department': 'FKN', 'group_number': '5'}
        self.input_data_update = {'surname': 'Журавлев', 'name': 'Павел', 'patronymic': 'Петрович', 'sex': 'мужской',
                    'platoon': '451', 'military_post': 'командир взвода', 'login': 'zhuravlev_p_p', 'password': 'oiu564123',
                    'department': 'FKN', 'group_number': '5'}


    def test_validated_data(self):
        validated_data = validate_student_data(self.input_data_correct)
        self.assertEqual(validated_data, self.input_data_correct)
        with self.assertRaises(ValidationError):
            invalid_data = validate_student_data(self.input_data_incorrect)


    def test_insert_new_student(self):
        validated_data = validate_student_data(self.input_data_correct)
        self.assertEqual(validated_data, self.input_data_correct)
        add_new_student_to_db(validated_data)
        student = get_student(2)
        self.assertIsNotNone(student)
        self.assertEqual(student.surname, self.input_data_correct['surname'])
        self.assertEqual(student.name, self.input_data_correct['name'])
        self.assertEqual(student.patronymic, self.input_data_correct['patronymic'])


    def test_update_student(self):
        validated_data = validate_student_data(self.input_data_correct)
        add_new_student_to_db(validated_data)
        updating_data = validate_student_data(self.input_data_update)
        self.assertEqual(validated_data, self.input_data_correct)
        update_existing_student(updating_data, 2)
        student = get_student(2)
        self.assertIsNotNone(student)
        self.assertEqual(student.surname, self.input_data_update['surname'])
        self.assertEqual(student.name, self.input_data_update['name'])
        self.assertEqual(student.patronymic, self.input_data_update['patronymic'])
        self.assertEqual(student.military_post, self.input_data_update['military_post'])


    def test_delete_student(self):
        validated_data = validate_student_data(self.input_data_correct)
        add_new_student_to_db(validated_data)
        delete_student(2)
        with self.assertRaises(Exception):
            student = get_student(2)





         
    


