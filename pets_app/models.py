from django.conf import settings
from django.db import models


class Pet(models.Model):

    class SexChoices(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        UNKNOWN = "UNKNOWN", "Unknown"

    pet_id = models.BigAutoField(primary_key=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="owner_id",
        related_name="pets",
    )

    name = models.CharField(
        max_length=100,
    )

    species = models.CharField(
        max_length=100,
    )

    breed = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    sex = models.CharField(
        max_length=7,
        choices=SexChoices.choices,
        default=SexChoices.UNKNOWN,
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
    )

    photo = models.ImageField(
        upload_to="pets/",
        db_column="photo_url",
        max_length=500,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "pets"

        # IMPORTANT:
        # MySQL table already exists.
        # Django must not try to create/drop/alter it.
        managed = False

        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.species})"