from rest_framework.routers import DefaultRouter

from .views import RatingsItemViewSet

router = DefaultRouter()
router.register(r"items", RatingsItemViewSet, basename="ratings-item")

urlpatterns = router.urls
