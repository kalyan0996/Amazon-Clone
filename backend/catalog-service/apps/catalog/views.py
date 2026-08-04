from rest_framework import viewsets, permissions

from .models import CatalogItem
from .serializers import CatalogItemSerializer


class CatalogItemViewSet(viewsets.ModelViewSet):
    """CRUD API for catalog. Replace with real business logic."""

    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    permission_classes = [permissions.IsAuthenticated]
