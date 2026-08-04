from rest_framework.routers import DefaultRouter

from .views import PricingItemViewSet

router = DefaultRouter()
router.register(r"items", PricingItemViewSet, basename="pricing-item")

urlpatterns = router.urls
