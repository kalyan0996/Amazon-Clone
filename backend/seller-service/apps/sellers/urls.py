from rest_framework.routers import DefaultRouter

from .views import SellersItemViewSet

router = DefaultRouter()
router.register(r"items", SellersItemViewSet, basename="sellers-item")

urlpatterns = router.urls
