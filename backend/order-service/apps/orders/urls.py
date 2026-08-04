from rest_framework.routers import DefaultRouter

from .views import OrdersItemViewSet

router = DefaultRouter()
router.register(r"items", OrdersItemViewSet, basename="orders-item")

urlpatterns = router.urls
