from rest_framework.routers import DefaultRouter

from .views import PaymentsItemViewSet

router = DefaultRouter()
router.register(r"items", PaymentsItemViewSet, basename="payments-item")

urlpatterns = router.urls
