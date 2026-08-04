from rest_framework.routers import DefaultRouter

from .views import AuthItemViewSet

router = DefaultRouter()
router.register(r"items", AuthItemViewSet, basename="auth-item")

urlpatterns = router.urls
