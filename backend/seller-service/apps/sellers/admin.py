from django.contrib import admin

from .models import SellersItem


@admin.register(SellersItem)
class SellersItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
