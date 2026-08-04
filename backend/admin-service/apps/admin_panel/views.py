from rest_framework import viewsets, permissions

from .models import AdminPanelItem
from .serializers import AdminPanelItemSerializer


class AdminPanelItemViewSet(viewsets.ModelViewSet):
    """CRUD API for admin_panel. Replace with real business logic."""

    queryset = AdminPanelItem.objects.all()
    serializer_class = AdminPanelItemSerializer
    permission_classes = [permissions.IsAuthenticated]
