from rest_framework.routers import DefaultRouter

from .views import NotificationsItemViewSet

router = DefaultRouter()
router.register(r"items", NotificationsItemViewSet, basename="notifications-item")

urlpatterns = router.urls
