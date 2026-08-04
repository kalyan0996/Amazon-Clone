from django.contrib import admin

from .models import AdminPanelItem


@admin.register(AdminPanelItem)
class AdminPanelItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
