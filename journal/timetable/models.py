from django.db import models
from users.models import TeacherProfile, Platoon, CourseDirection


class Subject(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete = models.DO_NOTHING)
    name = models.TextField()
    hours_count = models.IntegerField()
    form = models.TextChoices('экзамен', 'зачет')

    class Meta:
        db_table = 'subjects'


class SubjectClass(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.DO_NOTHING)
    platoon = models.ForeignKey(Platoon, on_delete = models.DO_NOTHING)
    class_date = models.DateTimeField()
    theme_number = models.IntegerField()
    theme_name = models.TextField()
    class_number = models.IntegerField()
    class_name = models.TextField()
    class_type = models.TextField()
    classroom = models.CharField(max_length=4)

    class Meta:
        db_table = 'subject_classes'


class DirectionsSubjects(models.Model):
    course_direction = models.ForeignKey(CourseDirection, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('course_direction'), ('subject'))
        db_table = 'directions_subjects'

