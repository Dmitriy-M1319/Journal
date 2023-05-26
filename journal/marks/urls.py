from rest_framework.routers import SimpleRouter

from marks.views import CeilViewSet


router = SimpleRouter()
router.register(r'^', CeilViewSet)

urlpatterns = []

urlpatterns += router.urls
