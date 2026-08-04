from rest_framework import viewsets, permissions

from .models import AuthItem
from .serializers import AuthItemSerializer


class AuthItemViewSet(viewsets.ModelViewSet):
    """CRUD API for auth. Replace with real business logic."""

    queryset = AuthItem.objects.all()
    serializer_class = AuthItemSerializer
    permission_classes = [permissions.IsAuthenticated]
