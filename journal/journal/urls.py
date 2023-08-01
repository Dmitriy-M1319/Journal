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
from django.urls import path, include, re_path
from users.views import *
from timetable.views import *
from marks.views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('students', include('users.urls.student')),
    path('teachers', include('users.urls.teacher')),
    path('platoons', include('users.urls.platoon')),
    path('subjects', include('timetable.urls.subject')),
    path('classes', include('timetable.urls.subjectclass')),
    path('directions', include('timetable.urls.direction')),
    path('ceils', include('marks.urls')),
    path('auth/', include('djoser.urls')),       
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name="schema")),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name="schema"),
]
