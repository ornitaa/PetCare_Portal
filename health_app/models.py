from django.db import models
from django.conf import settings
from pets_app.models import Pet


class MedicalRecord(models.Model):

    class RecordKind(models.TextChoices):
        CHECKUP = "CHECKUP", "Checkup"
        ILLNESS = "ILLNESS", "Illness"
        INJURY = "INJURY", "Injury"
        SURGERY = "SURGERY", "Surgery"
        DIAGNOSIS = "DIAGNOSIS", "Diagnosis"
        FOLLOW_UP = "FOLLOW_UP", "Follow-up"
        EMERGENCY = "EMERGENCY", "Emergency"
        OTHER = "OTHER", "Other"

    record_id = models.BigAutoField(primary_key=True)

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        db_column="pet_id",
        related_name="medical_records",
    )

    recorded_on = models.DateField()

    record_kind = models.CharField(
        max_length=20,
        choices=RecordKind.choices,
        default=RecordKind.OTHER,
    )

    diagnosis = models.TextField(
        blank=True,
        null=True,
    )

    care_notes = models.TextField(
        blank=True,
        null=True,
    )

    vet_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    attachment = models.FileField(
        upload_to="medical_records/",
        db_column="attachment_url",
        max_length=500,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "medical_records"
        managed = False
        ordering = ["-recorded_on", "-record_id"]

    def __str__(self):
        return f"{self.pet.name} - {self.record_kind} - {self.recorded_on}"


class Medication(models.Model):

    medication_id = models.BigAutoField(primary_key=True)

    record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        db_column="record_id",
        related_name="medications",
    )

    medication_name = models.CharField(
        max_length=150,
    )

    dose = models.CharField(
        max_length=100,
    )

    route = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    frequency = models.CharField(
        max_length=150,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "medications"
        managed = False
        ordering = ["-start_date", "-medication_id"]

    def __str__(self):
        return self.medication_name


class Vaccination(models.Model):
    vaccination_id = models.BigAutoField(primary_key=True)

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        db_column="pet_id",
        related_name="vaccinations",
    )

    vaccine_name = models.CharField(max_length=150)

    dose_label = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    administered_on = models.DateField()

    next_due_on = models.DateField(
        blank=True,
        null=True,
    )

    clinic_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vaccinations"
        managed = False
        ordering = ["-administered_on", "-vaccination_id"]

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine_name}"

class GrowthRecord(models.Model):
    growth_id = models.BigAutoField(primary_key=True)

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        db_column="pet_id",
        related_name="growth_records",
    )

    measured_on = models.DateField()

    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    height_cm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    milestone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "growth_records"
        managed = False
        ordering = ["-measured_on", "-growth_id"]

    def __str__(self):
        return f"{self.pet.name} - {self.measured_on}"

class CareReminder(models.Model):

    class ReminderKind(models.TextChoices):
        VET_APPOINTMENT = "VET_APPOINTMENT", "Vet appointment"
        MEDICATION = "MEDICATION", "Medication"
        VACCINATION = "VACCINATION", "Vaccination"
        GROOMING = "GROOMING", "Grooming"
        DEWORMING = "DEWORMING", "Deworming"
        FEEDING = "FEEDING", "Feeding"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    reminder_id = models.BigAutoField(primary_key=True)

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        db_column="pet_id",
        related_name="care_reminders",
    )
    vaccination = models.OneToOneField(
        "Vaccination",
        on_delete=models.CASCADE,
        db_column="vaccination_id",
        related_name="automatic_reminder",
        blank=True,
        null=True,
    )

    title = models.CharField(max_length=200)

    reminder_kind = models.CharField(
        max_length=30,
        choices=ReminderKind.choices,
    )

    remind_at = models.DateTimeField()

    details = models.TextField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    notification_sent_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "care_reminders"
        managed = False
        ordering = ["remind_at", "reminder_id"]

    def __str__(self):
        return f"{self.pet.name} - {self.title}"



class PushDevice(models.Model):

    device_id = models.BigAutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="push_devices",
    )

    firebase_fid = models.CharField(
        max_length=255,
        unique=True,
    )

    device_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    last_registered_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        managed = False
        db_table = "push_devices"

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.device_name or 'Browser'}"
        )