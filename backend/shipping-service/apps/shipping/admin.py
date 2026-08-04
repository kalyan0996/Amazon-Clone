from django.contrib import admin

from .models import ShippingItem


@admin.register(ShippingItem)
class ShippingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
