from rest_framework.routers import DefaultRouter

from .views import ShippingItemViewSet

router = DefaultRouter()
router.register(r"items", ShippingItemViewSet, basename="shipping-item")

urlpatterns = router.urls
