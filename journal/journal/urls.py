"""journal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import *
from timetable.views import *
from marks.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginView),
    path('logout/', logoutView),
    path('authtest/', getAuthUserView),
    path('students/', getStudentsView),
    path('student/<int:id>/', getStudentByIdView),
    path('teachers/', getTeachersView),
    path('teacher/<int:id>/', getTeacherByIdView),
    path('teacher/<int:id>/update/', updateTeacherView),
    path('teacher/<int:id>/delete/', deleteTeacherView),
    path('teacher/create/', createTeacherView),
    path('platoon/<int:id>/', getPlatoonByNumberView),
    path('student/<int:id>/platoon/', getPlatoonByStudentView),
    path('platoon/<int:id>/students/', getStudentsByPlatoonView),
    path('platoon/<int:id>/tutor/', getPlatoonTutorView),
    path('teacher/<int:id>/subjects/', getSubjectsForTeacherView),
    path('platoon/<int:id>/timetable/', getTimetableForPlatoonInDayView),
    path('teacher/<int:id>/classes/', getSubjectClassesForTeacherView),
    path('student/<int:id>/ceils/',  getJournalCeilsView),
    path('subject/<int:id>/ceils/', getCeilsBySubjectView),
    path('ceil/create/', createCeilView),
    path('ceil/<int:id>/update/', updateCeilView),
    path('ceil/<int:id>/delete/', deleteCeilView),
]
