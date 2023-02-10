from django.core.exceptions import ValidationError
from django.test import TestCase
from users.platoon_services import validateDataForPlatoon, addNewPlatoon, updateExistingPlatoon, deletePlatoonWithGraduation, getPlatoonByNumber
from users.teacher_services import addNewTeacherToDatabase, deleteTeacherFromDatabase, getTeacher, updateExistingTeacher, validateTeacherData
from users.student_services import *

from .models import Platoon, Teacher

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
        with self.assertRaises(Exception):
            teacher = getTeacher(1)



class PlatoonServicesTests(TestCase):
    def setUp(self) -> None:
        Teacher.objects.create(surname='Иванов', name='Иван',
                              patronymic='Иванович', military_rank='капитан',
                              military_post='преподаватель', cycle='Цикл 1',
                              role=1, login='ivanov_i_i', password='t12345678',
                              status=True)
        self.teacher = getTeacher(1)
        self.input_data_correct = {'platoon_number': '551', 'tutor': self.teacher.id, 'year': 2021, 'status': 'выпустился'}
        self.input_data_incorrect1 = {'platoon_number': '551', 'tutor': self.teacher.id, 'year': 2021, 'status': 'отчислен'}
        self.input_data_incorrect2 = {'platoon_number': '551', 'tutor': Teacher().id, 'year': 2021, 'status': 'выпустился'}


    def test_validated_data(self):
        validated_data1 = validateDataForPlatoon(self.input_data_correct) 
        self.assertEqual(validated_data1, self.input_data_correct)
        with self.assertRaises(ValidationError):
            validated_data2 = validateDataForPlatoon(self.input_data_incorrect1) 
        with self.assertRaises(ValidationError):
            validated_data3 = validateDataForPlatoon(self.input_data_incorrect2) 


    def test_insert_platoon(self):
        validated_data = validateDataForPlatoon(self.input_data_correct)
        addNewPlatoon(validated_data)
        platoon = getPlatoonByNumber(551)
        self.assertEqual(self.teacher, platoon.tutor)


    def test_update_platoon(self):
        Platoon.objects.create(platoon_number=451, tutor=self.teacher, year=2020, status='учится')
        self.input_data_correct = {'platoon_number': '451', 'tutor': self.teacher.id, 'year': 2021, 'status': 'выпустился'}
        platoon = getPlatoonByNumber(451)
        self.assertIsNotNone(platoon)
        self.assertEqual(platoon.platoon_number, 451)
        self.assertEqual(platoon.year, 2020)
        self.assertEqual(platoon.status, 'учится')
        validated_data = validateDataForPlatoon(self.input_data_correct)
        updateExistingPlatoon(validated_data, platoon.platoon_number)
        platoon = getPlatoonByNumber(451)
        self.assertIsNotNone(platoon)
        self.assertEqual(platoon.platoon_number, 451)
        self.assertEqual(platoon.year, 2021)


    def test_delete_platoon(self):
        Platoon.objects.create(platoon_number=451, tutor=self.teacher, year=2020, status='учится')
        platoon = getPlatoonByNumber(451)
        self.assertIsNotNone(platoon)
        deletePlatoonWithGraduation(platoon.platoon_number)
        platoon = getPlatoonByNumber(451)
        self.assertEqual(platoon.status, 'выпустился')


class StudentServicesTests(TestCase):
    def setUp(self) -> None:
        Teacher.objects.create(surname='Иванов', name='Иван',
                              patronymic='Иванович', military_rank='капитан',
                              military_post='преподаватель', cycle='Цикл 1',
                              role=1, login='ivanov_i_i', password='t12345678',
                              status=True)
        self.teacher = getTeacher(1)
        Platoon.objects.create(platoon_number=451, tutor=self.teacher, year=2020, status='учится')

        self.platoon = getPlatoonByNumber(451)
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
        validated_data = validateStudentData(self.input_data_correct)
        self.assertEqual(validated_data, self.input_data_correct)
        with self.assertRaises(ValidationError):
            invalid_data = validateStudentData(self.input_data_incorrect)


    def test_insert_new_student(self):
        validated_data = validateStudentData(self.input_data_correct)
        self.assertEqual(validated_data, self.input_data_correct)
        addNewStudent(validated_data)
        student = getStudent(1)
        self.assertIsNotNone(student)
        self.assertEqual(student.surname, self.input_data_correct['surname'])
        self.assertEqual(student.name, self.input_data_correct['name'])
        self.assertEqual(student.patronymic, self.input_data_correct['patronymic'])


    def test_update_student(self):
        validated_data = validateStudentData(self.input_data_correct)
        addNewStudent(validated_data)
        updating_data = validateStudentData(self.input_data_update)
        self.assertEqual(validated_data, self.input_data_correct)
        updateStudentInDb(updating_data, 1)
        student = getStudent(1)
        self.assertIsNotNone(student)
        self.assertEqual(student.surname, self.input_data_update['surname'])
        self.assertEqual(student.name, self.input_data_update['name'])
        self.assertEqual(student.patronymic, self.input_data_update['patronymic'])
        self.assertEqual(student.military_post, self.input_data_update['military_post'])
        self.assertEqual(student.login, self.input_data_update['login'])


    def test_delete_student(self):
        validated_data = validateStudentData(self.input_data_correct)
        addNewStudent(validated_data)
        deleteStudentFromDb(1)
        with self.assertRaises(Exception):
            student = getStudent(1)





         
    


