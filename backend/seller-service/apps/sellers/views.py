from rest_framework import viewsets, permissions

from .models import SellersItem
from .serializers import SellersItemSerializer


class SellersItemViewSet(viewsets.ModelViewSet):
    """CRUD API for sellers. Replace with real business logic."""

    queryset = SellersItem.objects.all()
    serializer_class = SellersItemSerializer
    permission_classes = [permissions.IsAuthenticated]
