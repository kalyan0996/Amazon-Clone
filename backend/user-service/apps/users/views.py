from rest_framework import viewsets, permissions

from .models import UsersItem
from .serializers import UsersItemSerializer


class UsersItemViewSet(viewsets.ModelViewSet):
    """CRUD API for users. Replace with real business logic."""

    queryset = UsersItem.objects.all()
    serializer_class = UsersItemSerializer
    permission_classes = [permissions.IsAuthenticated]
