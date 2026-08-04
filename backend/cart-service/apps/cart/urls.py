from rest_framework.routers import DefaultRouter

from .views import CartItemViewSet

router = DefaultRouter()
router.register(r"items", CartItemViewSet, basename="cart-item")

urlpatterns = router.urls
