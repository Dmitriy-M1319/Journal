from rest_framework.routers import SimpleRouter

from users.views import StudentProfileViewSet


router = SimpleRouter()
router.register(r'^', StudentProfileViewSet)

urlpatterns = []

urlpatterns += router.urls
