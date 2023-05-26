from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TeacherProfile, StudentProfile

admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
