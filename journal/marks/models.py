from django.db import models

from users.models import StudentProfile
from timetable.models import SubjectClass


class JournalCeil(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete = models.DO_NOTHING)
    subject_class = models.ForeignKey(SubjectClass, on_delete = models.DO_NOTHING)
    mark = models.IntegerField()
    attendance = models.CharField(max_length=10, default='')

    class Meta:
        db_table = 'journal_ceils'
