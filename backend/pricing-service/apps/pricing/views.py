from rest_framework import viewsets, permissions

from .models import PricingItem
from .serializers import PricingItemSerializer


class PricingItemViewSet(viewsets.ModelViewSet):
    """CRUD API for pricing. Replace with real business logic."""

    queryset = PricingItem.objects.all()
    serializer_class = PricingItemSerializer
    permission_classes = [permissions.IsAuthenticated]
