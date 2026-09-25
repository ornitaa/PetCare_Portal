from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "full_name",
        "email",
        "phone",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = (
        "full_name",
        "email",
        "phone",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "user_id",
        "password",
        "last_login",
        "created_at",
        "updated_at",
    )