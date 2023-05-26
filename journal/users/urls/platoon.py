from rest_framework.routers import SimpleRouter

from users.views import PlatoonViewSet


router = SimpleRouter()
router.register(r'^', PlatoonViewSet)

urlpatterns = []

urlpatterns += router.urls
