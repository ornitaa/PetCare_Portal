from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        "pet_id",
        "name",
        "species",
        "breed",
        "sex",
        "owner",
        "birth_date",
        "created_at",
    )

    list_filter = (
        "species",
        "sex",
    )

    search_fields = (
        "name",
        "species",
        "breed",
        "owner__full_name",
        "owner__email",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "pet_id",
        "created_at",
        "updated_at",
    )