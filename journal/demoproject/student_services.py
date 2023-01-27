"""
Модуль бизнес-логики для сущности студента
"""
from django.db.models.fields import CharField
from .models import Student, Platoon
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

def validateData(surname,
                 name,
                 patronymic,
                 sex,
                 platoon,
                 military_post,
                 login,
                 password,
                 department,
                 group_number):
    # прочитать про регулярные выражения и сделать проверки
    #raise Exception()
    return [surname, name, patronymic, sex, platoon, military_post, login, password, department, group_number]

def addStudent(data):
    new_student = Student()
    new_student.surname = data['surname']
    new_student.name = data['name']
    new_student.patronymic = data['patronymic']
    new_student.sex = data['sex']
    new_student.platoon = data['platoon']
    new_student.military_post = data['military_post']
    new_student.login = data['military_post']
    new_student.password = CharField(make_password(data['password']))
    new_student.department = data['department']
    new_student.group_number = data['group_number']
    new_student.active = CharField("учится")
    
    new_student.save()
    logger.info("New student was created successfully")
    





