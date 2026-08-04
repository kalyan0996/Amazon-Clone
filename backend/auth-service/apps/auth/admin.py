from django.contrib import admin

from .models import AuthItem


@admin.register(AuthItem)
class AuthItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
