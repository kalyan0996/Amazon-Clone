from rest_framework import viewsets, permissions

from .models import NotificationsItem
from .serializers import NotificationsItemSerializer


class NotificationsItemViewSet(viewsets.ModelViewSet):
    """CRUD API for notifications. Replace with real business logic."""

    queryset = NotificationsItem.objects.all()
    serializer_class = NotificationsItemSerializer
    permission_classes = [permissions.IsAuthenticated]
