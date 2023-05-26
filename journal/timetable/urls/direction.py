from rest_framework.routers import SimpleRouter

from timetable.views import CourseDirectionViewSet


router = SimpleRouter()
router.register(r'^', CourseDirectionViewSet)

urlpatterns = []

urlpatterns += router.urls
