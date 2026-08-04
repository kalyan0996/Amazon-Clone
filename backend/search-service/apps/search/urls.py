from rest_framework.routers import DefaultRouter

from .views import SearchItemViewSet

router = DefaultRouter()
router.register(r"items", SearchItemViewSet, basename="search-item")

urlpatterns = router.urls
