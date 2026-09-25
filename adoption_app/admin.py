from django.contrib import admin

from .models import AdoptionListing


@admin.register(AdoptionListing)
class AdoptionListingAdmin(admin.ModelAdmin):

    list_display = (
        "listing_id",
        "pet",
        "location",
        "listing_status",
        "listed_at",
        "closed_at",
    )

    list_filter = (
        "listing_status",
        "listed_at",
    )

    search_fields = (
        "pet__name",
        "pet__owner__full_name",
        "location",
        "description",
    )