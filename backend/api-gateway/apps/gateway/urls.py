from rest_framework.routers import DefaultRouter

from .views import GatewayItemViewSet

router = DefaultRouter()
router.register(r"items", GatewayItemViewSet, basename="gateway-item")

urlpatterns = router.urls
