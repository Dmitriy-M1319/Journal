from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TeacherProfile, StudentProfile

admin.site.register(CustomUser, UserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
