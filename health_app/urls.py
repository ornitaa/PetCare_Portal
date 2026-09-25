from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.medical_record_list,
        name="medical_record_list",
    ),

    path(
        "add/",
        views.medical_record_add,
        name="medical_record_add",
    ),

    path(
        "<int:record_id>/",
        views.medical_record_detail,
        name="medical_record_detail",
    ),

    path(
        "<int:record_id>/edit/",
        views.medical_record_edit,
        name="medical_record_edit",
    ),

    path(
        "<int:record_id>/delete/",
        views.medical_record_delete,
        name="medical_record_delete",
    ),

    path(
        "<int:record_id>/medications/add/",
        views.medication_add,
        name="medication_add",
    ),

    path(
        "<int:record_id>/medications/<int:medication_id>/edit/",
        views.medication_edit,
        name="medication_edit",
    ),

    path(
        "<int:record_id>/medications/<int:medication_id>/delete/",
        views.medication_delete,
        name="medication_delete",
    ),
    path(
    "vaccinations/",
    views.vaccination_list,
    name="vaccination_list",
),

    path(
      "vaccinations/add/",
      views.vaccination_add,
      name="vaccination_add",
    ),

    path(
     "vaccinations/<int:vaccination_id>/edit/",
     views.vaccination_edit,
     name="vaccination_edit",
    ),

    path(
        "vaccinations/<int:vaccination_id>/delete/",
     views.vaccination_delete,
     name="vaccination_delete",
    ),
    path(
    "growth/",
    views.growth_list,
    name="growth_list",
    ),

    path(
        "growth/add/",
        views.growth_add,
        name="growth_add",
    ),

    path(
        "growth/<int:growth_id>/edit/",
        views.growth_edit,
        name="growth_edit",
    ),

    path(
        "growth/<int:growth_id>/delete/",
        views.growth_delete,
        name="growth_delete",
    ),
    path(
    "reminders/",
    views.reminder_list,
    name="reminder_list",
    ),

    path(
     "reminders/add/",
     views.reminder_add,
     name="reminder_add",
    ),

    path(
        "reminders/<int:reminder_id>/edit/",
        views.reminder_edit,
        name="reminder_edit",
    ),

    path(
        "reminders/<int:reminder_id>/complete/",
        views.reminder_complete,
        name="reminder_complete",
    ),

    path(
        "reminders/<int:reminder_id>/cancel/",
        views.reminder_cancel,
        name="reminder_cancel",
    ),

    path(
        "reminders/<int:reminder_id>/reopen/",
        views.reminder_reopen,
        name="reminder_reopen",
    ),

    path(
     "reminders/<int:reminder_id>/delete/",
        views.reminder_delete,
        name="reminder_delete",
    ),
]