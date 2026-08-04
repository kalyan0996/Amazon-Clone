from django.contrib import admin

from .models import GatewayItem


@admin.register(GatewayItem)
class GatewayItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
