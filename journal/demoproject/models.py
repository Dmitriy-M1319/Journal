from django.db import models


# Модель преподавателя
class Teacher(models.Model):
    # Фамилия
    surname = models.CharField(max_length=40)
    # Имя 
    name = models.CharField(max_length=40)
    # Отчество
    patronymic = models.CharField(max_length=40)
    # Воинское звание
    military_rank = models.CharField(max_length=20)
    # Воинская должность
    military_post = models.CharField(max_length=255)
    # Цикл
    cycle = models.CharField(max_length=255)
    # Логин в учетной системе
    login = models.CharField(max_length=30)
    # Пароль (в хэшированном виде)
    password = models.CharField(max_length=255)
    # Статус преподавателя (работает или уволен)
    status = models.BooleanField()

# Модель взвода
class Platoon(models.Model):
    # Номер взвода (выступает первичным ключом)
    platoon_number = models.IntegerField(primary_key=True)
    # Куратор взвода (ссылка на преподавателя)
    tutor = models.OneToOneField(Teacher, on_delete = models.DO_NOTHING)
    # Год набора
    year = models.IntegerField()


# Модель студента
class Student(models.Model):
    # Фамилия
    surname = models.CharField(max_length=40)
    # Имя 
    name = models.CharField(max_length=40)
    # Отчество
    patronymic = models.CharField(max_length=40)
    # Пол
    sex = models.CharField(max_length=10)
    # Номер взвода (ссылка на взвод)
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    # Должность во взводе
    military_post = models.CharField(max_length=255)
    # Логин в учетной системе
    login = models.CharField(max_length=30)
    # Пароль (в хэшированном виде)
    password = models.CharField(max_length=255)
    # Фотография студента
    # photo = models.ImageField()
    # Факультет в гражданском вузе
    department = models.CharField(max_length=255)
    # Номер группы на факультете
    group_number = models.IntegerField()
    # Статус студента (учится, выпустился или отчислен)
    active = models.CharField(max_length=30)


# Модель предмета
class Subject(models.Model):
    # Преподаватель (ссылка на преподавателя)
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    # Название предмета
    name = models.CharField(max_length=100)
    # Количество часов
    hours_count = models.IntegerField()
    # Форма отчетности (экзамен, зачет)
    form = models.CharField(max_length=15)


# Модель занятия
class SubjectClass(models.Model):
    # Предмет, по которому было занятие
    subject = models.ForeignKey(Subject, on_delete = models.DO_NOTHING)
    # Взвод, у которого должно быть занятие
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    # Дата занятия
    date = models.DateField()
    # Номер темы
    theme_number = models.IntegerField()
    # Название темы
    theme_name = models.CharField(max_length=255)
    # Номер занятия
    class_number = models.IntegerField()
    # Название занятия
    class_name = models.CharField(max_length=255)
    # Тип занятия (лекция, семинар, контрольное занятие)
    class_type = models.CharField(max_length=30)
    # Номер аудитории
    classroom = models.IntegerField()


# Модель журнальной записи (клеточка в обычном журнале)
class JournalCeil(models.Model):
    # Студент, которому принадлежит клеточка
    student = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
    # Занятие, за которое ставится оценка
    subject_class = models.OneToOneField(SubjectClass, on_delete = models.DO_NOTHING)
    # Оценка
    mark = models.IntegerField()
    # Посещаемость (был, неуваж. причина, болен)
    attendance = models.CharField(max_length=10)
    # Оставим место для справки в случае болезни





