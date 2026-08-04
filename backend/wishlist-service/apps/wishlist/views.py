from rest_framework import viewsets, permissions

from .models import WishlistItem
from .serializers import WishlistItemSerializer


class WishlistItemViewSet(viewsets.ModelViewSet):
    """CRUD API for wishlist. Replace with real business logic."""

    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]
