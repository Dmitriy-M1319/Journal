from django.db import models
from users.models import StudentProfile
from timetable.models import SubjectClass


class JournalCeil(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete = models.DO_NOTHING)
    subject_class = models.ForeignKey(SubjectClass, on_delete = models.DO_NOTHING)
    mark = models.IntegerField()
    # Посещаемость (был, неуваж. причина, болен)
    attendance = models.CharField(max_length=10)

    class Meta:
        db_table = 'journal_ceils'



