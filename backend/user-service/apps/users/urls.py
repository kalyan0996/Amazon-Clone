from rest_framework.routers import DefaultRouter

from .views import UsersItemViewSet

router = DefaultRouter()
router.register(r"items", UsersItemViewSet, basename="users-item")

urlpatterns = router.urls
