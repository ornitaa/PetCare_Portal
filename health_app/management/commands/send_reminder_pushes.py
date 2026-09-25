from django.core.management.base import BaseCommand
from django.utils import timezone

from firebase_admin import messaging

from health_app.firebase_service import get_firebase_app
from health_app.models import CareReminder, PushDevice


class Command(BaseCommand):

    help = "Send browser push notifications for due care reminders."


    def handle(self, *args, **options):

        firebase_app = get_firebase_app()

        now = timezone.now()

        self.stdout.write(
            f"Checking reminders at: {now}"
        )

        reminders = (
            CareReminder.objects
            .filter(
                status=CareReminder.Status.PENDING,
                notification_sent_at__isnull=True,
                remind_at__lte=now,
            )
            .select_related(
                "pet",
                "pet__owner",
            )
            .order_by("remind_at")
        )


        if not reminders.exists():

            self.stdout.write(
                self.style.WARNING(
                    "No unsent due reminders found."
                )
            )

            return


        self.stdout.write(
            f"Found {reminders.count()} due reminder(s)."
        )


        sent_reminders = 0


        for reminder in reminders:

            self.stdout.write("")

            self.stdout.write(
                (
                    f"Reminder #{reminder.reminder_id}: "
                    f"{reminder.title}"
                )
            )

            self.stdout.write(
                f"Scheduled for: {reminder.remind_at}"
            )


            devices = (
                PushDevice.objects
                .filter(
                    user=reminder.pet.owner,
                    is_active=True,
                )
            )


            if not devices.exists():

                self.stdout.write(
                    self.style.WARNING(
                        "No active push device found."
                    )
                )

                continue


            successful_devices = 0


            for device in devices:

                title = (
                    f"Reminder for {reminder.pet.name}"
                )


                body = reminder.title


                if reminder.details:

                    body += (
                        f" — {reminder.details}"
                    )


                message = messaging.Message(

                    data={
                        "url": "/reminders/",

                        "reminder_id": str(
                            reminder.reminder_id
                        ),

                        "tag": (
                            "petcare-reminder-"
                            f"{reminder.reminder_id}"
                        ),
                    },


                    webpush=messaging.WebpushConfig(

                        headers={
                            "Urgency": "high",
                        },

                        notification=(
                            messaging.WebpushNotification(

                                title=title,

                                body=body,

                                tag=(
                                    "petcare-reminder-"
                                    f"{reminder.reminder_id}"
                                ),

                                data={
                                    "url": "/reminders/"
                                },
                            )
                        ),
                    ),


                    fid=device.firebase_fid,
                )


                self.stdout.write(
                    (
                        "Sending to device "
                        f"#{device.device_id}..."
                    )
                )


                try:

                    result = messaging.send_each(
                        [message],
                        app=firebase_app,
                    )


                    response = result.responses[0]


                    if response.success:

                        successful_devices += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                (
                                    "FCM accepted notification "
                                    f"for device "
                                    f"#{device.device_id}"
                                )
                            )
                        )

                        self.stdout.write(
                            (
                                "Message ID: "
                                f"{response.message_id}"
                            )
                        )


                    else:

                        self.stdout.write(
                            self.style.ERROR(
                                (
                                    "FCM rejected notification "
                                    f"for device "
                                    f"#{device.device_id}"
                                )
                            )
                        )

                        self.stdout.write(
                            self.style.ERROR(
                                str(response.exception)
                            )
                        )


                        if isinstance(
                            response.exception,
                            messaging.UnregisteredError,
                        ):

                            device.is_active = False

                            device.save(
                                update_fields=[
                                    "is_active"
                                ]
                            )

                            self.stdout.write(
                                self.style.WARNING(
                                    (
                                        "The old Firebase "
                                        "registration was "
                                        "deactivated."
                                    )
                                )
                            )


                except Exception as exc:

                    self.stdout.write(
                        self.style.ERROR(
                            "Firebase send failed:"
                        )
                    )

                    self.stdout.write(
                        self.style.ERROR(
                            repr(exc)
                        )
                    )


            if successful_devices > 0:

                reminder.notification_sent_at = (
                    timezone.now()
                )

                reminder.save(
                    update_fields=[
                        "notification_sent_at"
                    ]
                )


                sent_reminders += 1


                self.stdout.write(
                    self.style.SUCCESS(
                        (
                            f"Reminder "
                            f"#{reminder.reminder_id} "
                            "marked as notified."
                        )
                    )
                )


        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Finished. "
                    f"{sent_reminders} reminder(s) "
                    "successfully pushed."
                )
            )
        )