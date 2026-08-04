from rest_framework.routers import DefaultRouter

from .views import AnalyticsItemViewSet

router = DefaultRouter()
router.register(r"items", AnalyticsItemViewSet, basename="analytics-item")

urlpatterns = router.urls
