from rest_framework.routers import SimpleRouter

from timetable.views import SubjectClassViewSet


router = SimpleRouter()
router.register(r'^', SubjectClassViewSet)

urlpatterns = []

urlpatterns += router.urls
