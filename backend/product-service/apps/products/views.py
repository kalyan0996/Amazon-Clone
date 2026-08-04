from rest_framework import viewsets, permissions

from .models import ProductsItem
from .serializers import ProductsItemSerializer


class ProductsItemViewSet(viewsets.ModelViewSet):
    """CRUD API for products. Replace with real business logic."""

    queryset = ProductsItem.objects.all()
    serializer_class = ProductsItemSerializer
    permission_classes = [permissions.IsAuthenticated]
