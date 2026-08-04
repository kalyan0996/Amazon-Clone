from rest_framework import viewsets, permissions

from .models import ShippingItem
from .serializers import ShippingItemSerializer


class ShippingItemViewSet(viewsets.ModelViewSet):
    """CRUD API for shipping. Replace with real business logic."""

    queryset = ShippingItem.objects.all()
    serializer_class = ShippingItemSerializer
    permission_classes = [permissions.IsAuthenticated]
