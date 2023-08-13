from rest_framework.routers import SimpleRouter

from marks.views import JournalCeilViewSet


router = SimpleRouter()
router.register(r'^', JournalCeilViewSet)

urlpatterns = []

urlpatterns += router.urls
