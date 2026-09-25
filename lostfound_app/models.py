from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
from pets_app.models import Pet


class PetReport(models.Model):

    class ReportType(models.TextChoices):
        LOST = "LOST", "Lost"
        FOUND = "FOUND", "Found"

    class ReportStatus(models.TextChoices):
        OPEN = "OPEN", "Open"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    report_id = models.BigAutoField(
        primary_key=True
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="reporter_id",
        related_name="pet_reports",
    )

    pet = models.ForeignKey(
        Pet,
        on_delete=models.SET_NULL,
        db_column="pet_id",
        related_name="reports",
        blank=True,
        null=True,
    )

    report_type = models.CharField(
        max_length=10,
        choices=ReportType.choices,
    )

    description = models.TextField()

    location = models.CharField(
        max_length=255,
    )

    incident_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    photo = CloudinaryField(
    "photo",
    resource_type="image",
    asset_folder="petcare/lost_found",
    use_asset_folder_as_public_id_prefix=True,
    db_column="photo_url",
    blank=True,
    null=True,
    )

    report_status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.OPEN,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "pet_reports"
        managed = False
        ordering = [
            "-created_at",
            "-report_id",
        ]

    def __str__(self):
        return (
            f"{self.get_report_type_display()} "
            f"report #{self.report_id}"
        )