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
from django.urls import path, include, re_path
from users.views import *
from timetable.views import *
from marks.views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/students', include('users.urls.student')),
    path('api/v1/teachers', include('users.urls.teacher')),
    path('api/v1/platoons', include('users.urls.platoon')),
    path('api/v1/subjects', include('timetable.urls.subject')),
    path('api/v1/classes', include('timetable.urls.subjectclass')),
    path('api/v1/directions', include('timetable.urls.direction')),
    path('api/v1/ceils', include('marks.urls')),
    path('api/v1/auth/', include('djoser.urls')),       
    re_path(r'^api/v1/auth/', include('djoser.urls.authtoken')),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name="schema")),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name="schema"),
]
