from rest_framework.routers import DefaultRouter

from .views import RecommendationsItemViewSet

router = DefaultRouter()
router.register(r"items", RecommendationsItemViewSet, basename="recommendations-item")

urlpatterns = router.urls
