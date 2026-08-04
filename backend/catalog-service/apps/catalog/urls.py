from rest_framework.routers import DefaultRouter

from .views import CatalogItemViewSet

router = DefaultRouter()
router.register(r"items", CatalogItemViewSet, basename="catalog-item")

urlpatterns = router.urls
