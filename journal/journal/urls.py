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
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Блок подключения Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Swagger API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter()
router.register(r'students', StudentProfileViewSet, basename='students')
router.register(r'teachers', TeacherProfileViewSet, basename='teachers')
router.register(r'platoons', PlatoonViewSet, basename='platoons')
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'classes', SubjectClassViewSet, basename='classes')
router.register(r'ceils', CeilViewSet, basename='ceils')
router.register(r'directions', CourseDirectionViewSet, basename='directions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/user/<int:pk>/teacher', UserViewSet.as_view({'teacher_profile'})),
    path('api/v1/user/<int:pk>/student', UserViewSet.as_view({'student_profile'})),
    path('api/v1/auth/', include('djoser.urls')),       
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
