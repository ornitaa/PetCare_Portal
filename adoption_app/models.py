from django.db import models

from pets_app.models import Pet


class AdoptionListing(models.Model):

    class ListingStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        ADOPTED = "ADOPTED", "Adopted"
        CLOSED = "CLOSED", "Closed"

    listing_id = models.BigAutoField(
        primary_key=True
    )

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        db_column="pet_id",
        related_name="adoption_listings",
    )

    description = models.TextField()

    location = models.CharField(
        max_length=255,
    )

    listing_status = models.CharField(
        max_length=20,
        choices=ListingStatus.choices,
        default=ListingStatus.ACTIVE,
    )

    listed_at = models.DateTimeField()

    closed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "adoption_listings"
        managed = False
        ordering = [
            "-listed_at",
            "-listing_id",
        ]

    def __str__(self):
        return f"{self.pet.name} - {self.get_listing_status_display()}"