from django.contrib import admin

from .models import UsersItem


@admin.register(UsersItem)
class UsersItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
