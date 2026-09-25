from django.urls import path

from . import views


urlpatterns = [
    path(
        "vaccinations/",
        views.vaccination_overview,
        name="vaccination_overview",
    ),

    path(
        "reminders/",
        views.reminder_overview,
        name="reminder_overview",
    ),
    path(
    "notifications/",
    views.notification_settings,
    name="notification_settings",
    ),

    path(
        "push/register/",
        views.register_push_device,
        name="register_push_device",
    ),

    path(
        "push/unregister/",
        views.unregister_push_device,
        name="unregister_push_device",
    ),
]