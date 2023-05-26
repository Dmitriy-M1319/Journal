
from rest_framework.routers import SimpleRouter

from users.views import TeacherProfileViewSet


router = SimpleRouter()
router.register(r'^', TeacherProfileViewSet)

urlpatterns = []

urlpatterns += router.urls
