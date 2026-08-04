from rest_framework import viewsets, permissions

from .models import OrdersItem
from .serializers import OrdersItemSerializer


class OrdersItemViewSet(viewsets.ModelViewSet):
    """CRUD API for orders. Replace with real business logic."""

    queryset = OrdersItem.objects.all()
    serializer_class = OrdersItemSerializer
    permission_classes = [permissions.IsAuthenticated]
