from datetime import datetime, time, timedelta

from django.utils import timezone

from .models import CareReminder


VACCINATION_REMINDER_HOUR = 9
VACCINATION_REMINDER_DAYS_BEFORE = 1


def get_vaccination_reminder_time(vaccination):
    """
    Schedule the automatic vaccination reminder
    1 day before next_due_on at 9:00 AM local time.
    """

    reminder_date = (
        vaccination.next_due_on
        - timedelta(days=VACCINATION_REMINDER_DAYS_BEFORE)
    )

    naive_datetime = datetime.combine(
        reminder_date,
        time(hour=VACCINATION_REMINDER_HOUR),
    )

    return timezone.make_aware(
        naive_datetime,
        timezone.get_current_timezone(),
    )


def sync_vaccination_reminder(vaccination):
    """
    Create, update, or remove the automatic CareReminder
    associated with a vaccination.
    """

    existing_reminder = CareReminder.objects.filter(
        vaccination=vaccination
    ).first()

    # --------------------------------------------------------
    # No next due date -> no automatic reminder
    # --------------------------------------------------------

    if not vaccination.next_due_on:
        if existing_reminder:
            existing_reminder.delete()

        return None


    remind_at = get_vaccination_reminder_time(vaccination)

    title = f"{vaccination.vaccine_name} vaccination due"

    details = (
        f"{vaccination.vaccine_name} vaccination for "
        f"{vaccination.pet.name} is due on "
        f"{vaccination.next_due_on.strftime('%B %d, %Y')}."
    )


    # --------------------------------------------------------
    # Update existing automatic reminder
    # --------------------------------------------------------

    if existing_reminder:

        schedule_changed = (
            existing_reminder.remind_at != remind_at
        )

        existing_reminder.pet = vaccination.pet
        existing_reminder.title = title
        existing_reminder.reminder_kind = "VACCINATION"
        existing_reminder.remind_at = remind_at
        existing_reminder.details = details


        # If the due date changed, make the reminder usable again.
        if schedule_changed:
            existing_reminder.status = "PENDING"
            existing_reminder.completed_at = None
            existing_reminder.notification_sent_at = None


        existing_reminder.save()

        return existing_reminder


    # --------------------------------------------------------
    # Create new automatic reminder
    # --------------------------------------------------------

    reminder = CareReminder.objects.create(
        pet=vaccination.pet,
        vaccination=vaccination,
        title=title,
        reminder_kind="VACCINATION",
        remind_at=remind_at,
        details=details,
        status="PENDING",
        completed_at=None,
        notification_sent_at=None,
    )

    return reminder