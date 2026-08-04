from rest_framework.routers import DefaultRouter

from .views import ProductsItemViewSet

router = DefaultRouter()
router.register(r"items", ProductsItemViewSet, basename="products-item")

urlpatterns = router.urls
