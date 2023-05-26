from rest_framework.routers import SimpleRouter

from timetable.views import SubjectViewSet


router = SimpleRouter()
router.register(r'^', SubjectViewSet)

urlpatterns = []

urlpatterns += router.urls
