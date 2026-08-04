from rest_framework.routers import DefaultRouter

from .views import AdminPanelItemViewSet

router = DefaultRouter()
router.register(r"items", AdminPanelItemViewSet, basename="admin_panel-item")

urlpatterns = router.urls
