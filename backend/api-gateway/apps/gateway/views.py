from rest_framework import viewsets, permissions

from .models import GatewayItem
from .serializers import GatewayItemSerializer


class GatewayItemViewSet(viewsets.ModelViewSet):
    """CRUD API for gateway. Replace with real business logic."""

    queryset = GatewayItem.objects.all()
    serializer_class = GatewayItemSerializer
    permission_classes = [permissions.AllowAny]
