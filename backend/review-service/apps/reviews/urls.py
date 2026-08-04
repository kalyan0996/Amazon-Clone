from rest_framework.routers import DefaultRouter

from .views import ReviewsItemViewSet

router = DefaultRouter()
router.register(r"items", ReviewsItemViewSet, basename="reviews-item")

urlpatterns = router.urls
