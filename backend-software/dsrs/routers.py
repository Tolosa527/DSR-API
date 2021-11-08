from rest_framework.routers import DefaultRouter
from dsrs.views import DSRViewSet, ResourceViewSet

router = DefaultRouter()

router.register(r"dsrs", DSRViewSet)
router.register(r"resource/percentile", ResourceViewSet)

urlpatterns = router.urls
