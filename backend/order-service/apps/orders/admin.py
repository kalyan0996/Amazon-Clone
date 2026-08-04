from django.contrib import admin

from .models import OrdersItem


@admin.register(OrdersItem)
class OrdersItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
