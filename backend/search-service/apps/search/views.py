from rest_framework import viewsets, permissions

from .models import SearchItem
from .serializers import SearchItemSerializer


class SearchItemViewSet(viewsets.ModelViewSet):
    """CRUD API for search. Replace with real business logic."""

    queryset = SearchItem.objects.all()
    serializer_class = SearchItemSerializer
    permission_classes = [permissions.IsAuthenticated]
