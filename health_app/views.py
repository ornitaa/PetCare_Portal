from django.shortcuts import render
from .vaccination_reminders import sync_vaccination_reminder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from datetime import date
from django.utils import timezone
from pets_app.models import Pet
import json
from io import StringIO
import os
import secrets

from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import PushDevice
from .forms import (
    MedicalRecordForm,
    MedicationForm,
    VaccinationForm,
    GrowthRecordForm,
    CareReminderForm,
)

from .models import (
    MedicalRecord,
    Medication,
    Vaccination,
    GrowthRecord,
    CareReminder,
)


def get_owned_pet(request, pet_id):
    return get_object_or_404(
        Pet,
        pet_id=pet_id,
        owner=request.user,
    )


@login_required
def medical_record_list(request, pet_id):

    pet = get_owned_pet(request, pet_id)

    records = (
        MedicalRecord.objects
        .filter(pet=pet)
        .prefetch_related("medications")
        .order_by("-recorded_on", "-record_id")
    )

    return render(
        request,
        "health_app/medical_record_list.html",
        {
            "pet": pet,
            "records": records,
        },
    )


@login_required
def medical_record_add(request, pet_id):

    pet = get_owned_pet(request, pet_id)

    if request.method == "POST":

        form = MedicalRecordForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            record = form.save(commit=False)
            record.pet = pet
            record.save()

            messages.success(
                request,
                f"Medical record added for {pet.name}.",
            )

            return redirect(
                "medical_record_detail",
                pet_id=pet.pet_id,
                record_id=record.record_id,
            )

    else:
        form = MedicalRecordForm()

    return render(
        request,
        "health_app/medical_record_form.html",
        {
            "pet": pet,
            "form": form,
            "page_title": "Add medical record",
            "button_text": "Save medical record",
        },
    )


@login_required
def medical_record_detail(request, pet_id, record_id):

    pet = get_owned_pet(request, pet_id)

    record = get_object_or_404(
        MedicalRecord.objects.prefetch_related("medications"),
        record_id=record_id,
        pet=pet,
    )

    return render(
        request,
        "health_app/medical_record_detail.html",
        {
            "pet": pet,
            "record": record,
        },
    )


@login_required
def medical_record_edit(request, pet_id, record_id):

    pet = get_owned_pet(request, pet_id)

    record = get_object_or_404(
        MedicalRecord,
        record_id=record_id,
        pet=pet,
    )

    if request.method == "POST":

        form = MedicalRecordForm(
            request.POST,
            request.FILES,
            instance=record,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Medical record updated successfully.",
            )

            return redirect(
                "medical_record_detail",
                pet_id=pet.pet_id,
                record_id=record.record_id,
            )

    else:
        form = MedicalRecordForm(instance=record)

    return render(
        request,
        "health_app/medical_record_form.html",
        {
            "pet": pet,
            "record": record,
            "form": form,
            "page_title": "Edit medical record",
            "button_text": "Save changes",
        },
    )


@login_required
def medical_record_delete(request, pet_id, record_id):

    pet = get_owned_pet(request, pet_id)

    record = get_object_or_404(
        MedicalRecord,
        record_id=record_id,
        pet=pet,
    )

    if request.method == "POST":

        record.delete()

        messages.success(
            request,
            "Medical record deleted.",
        )

        return redirect(
            "medical_record_list",
            pet_id=pet.pet_id,
        )

    return render(
        request,
        "health_app/medical_record_delete.html",
        {
            "pet": pet,
            "record": record,
        },
    )


@login_required
def medication_add(request, pet_id, record_id):

    pet = get_owned_pet(request, pet_id)

    record = get_object_or_404(
        MedicalRecord,
        record_id=record_id,
        pet=pet,
    )

    if request.method == "POST":

        form = MedicationForm(request.POST)

        if form.is_valid():

            medication = form.save(commit=False)
            medication.record = record
            medication.save()

            messages.success(
                request,
                f"{medication.medication_name} added.",
            )

            return redirect(
                "medical_record_detail",
                pet_id=pet.pet_id,
                record_id=record.record_id,
            )

    else:
        form = MedicationForm()

    return render(
        request,
        "health_app/medication_form.html",
        {
            "pet": pet,
            "record": record,
            "form": form,
            "page_title": "Add medication",
            "button_text": "Add medication",
        },
    )


@login_required
def medication_edit(
    request,
    pet_id,
    record_id,
    medication_id,
):

    pet = get_owned_pet(request, pet_id)

    record = get_object_or_404(
        MedicalRecord,
        record_id=record_id,
        pet=pet,
    )

    medication = get_object_or_404(
        Medication,
        medication_id=medication_id,
        record=record,
    )

    if request.method == "POST":

        form = MedicationForm(
            request.POST,
            instance=medication,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Medication updated.",
            )

            return redirect(
                "medical_record_detail",
                pet_id=pet.pet_id,
                record_id=record.record_id,
            )

    else:
        form = MedicationForm(instance=medication)

    return render(
        request,
        "health_app/medication_form.html",
        {
            "pet": pet,
            "record": record,
            "medication": medication,
            "form": form,
            "page_title": "Edit medication",
            "button_text": "Save changes",
        },
    )


@login_required
def medication_delete(
    request,
    pet_id,
    record_id,
    medication_id,
):

    pet = get_owned_pet(request, pet_id)

    record = get_object_or_404(
        MedicalRecord,
        record_id=record_id,
        pet=pet,
    )

    medication = get_object_or_404(
        Medication,
        medication_id=medication_id,
        record=record,
    )

    if request.method == "POST":

        medication.delete()

        messages.success(
            request,
            "Medication removed.",
        )

        return redirect(
            "medical_record_detail",
            pet_id=pet.pet_id,
            record_id=record.record_id,
        )

    return render(
        request,
        "health_app/medication_delete.html",
        {
            "pet": pet,
            "record": record,
            "medication": medication,
        },
    )

@login_required
def vaccination_list(request, pet_id):
    pet = get_owned_pet(request, pet_id)

    vaccinations = Vaccination.objects.filter(
        pet=pet
    ).order_by(
        "-administered_on",
        "-vaccination_id",
    )

    return render(
        request,
        "health_app/vaccination_list.html",
        {
            "pet": pet,
            "vaccinations": vaccinations,
        },
    )


@login_required
def vaccination_add(request, pet_id):
    pet = get_owned_pet(request, pet_id)

    if request.method == "POST":
        form = VaccinationForm(request.POST)

        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.pet = pet
            vaccination.save()

            # Create automatic vaccination reminder
            sync_vaccination_reminder(vaccination)

            messages.success(
                request,
                f"{vaccination.vaccine_name} vaccination added.",
            )

            return redirect(
                "vaccination_list",
                pet_id=pet.pet_id,
            )

    else:
        form = VaccinationForm()

    return render(
        request,
        "health_app/vaccination_form.html",
        {
            "pet": pet,
            "form": form,
            "page_title": "Add vaccination",
            "button_text": "Save vaccination",
        },
    )


@login_required
def vaccination_edit(
    request,
    pet_id,
    vaccination_id,
):
    pet = get_owned_pet(request, pet_id)

    vaccination = get_object_or_404(
        Vaccination,
        vaccination_id=vaccination_id,
        pet=pet,
    )

    if request.method == "POST":
        form = VaccinationForm(
            request.POST,
            instance=vaccination,
        )

        if form.is_valid():
            vaccination = form.save()

            # Update/create/delete automatic reminder
            sync_vaccination_reminder(vaccination)

            messages.success(
                request,
                "Vaccination updated.",
            )

            return redirect(
                "vaccination_list",
                pet_id=pet.pet_id,
            )

    else:
        form = VaccinationForm(
            instance=vaccination,
        )

    return render(
        request,
        "health_app/vaccination_form.html",
        {
            "pet": pet,
            "vaccination": vaccination,
            "form": form,
            "page_title": "Edit vaccination",
            "button_text": "Save changes",
        },
    )

@login_required
def vaccination_delete(
    request,
    pet_id,
    vaccination_id,
):
    pet = get_owned_pet(request, pet_id)

    vaccination = get_object_or_404(
        Vaccination,
        vaccination_id=vaccination_id,
        pet=pet,
    )

    if request.method == "POST":
        vaccination.delete()

        messages.success(
            request,
            "Vaccination record deleted.",
        )

        return redirect(
            "vaccination_list",
            pet_id=pet.pet_id,
        )

    return render(
        request,
        "health_app/vaccination_delete.html",
        {
            "pet": pet,
            "vaccination": vaccination,
        },
    )

@login_required
def vaccination_overview(request):
    today = date.today()

    all_vaccinations = (
        Vaccination.objects
        .filter(pet__owner=request.user)
        .select_related("pet")
    )

    overdue_vaccinations = (
        all_vaccinations
        .filter(
            next_due_on__isnull=False,
            next_due_on__lt=today,
        )
        .order_by("next_due_on")
    )

    upcoming_vaccinations = (
        all_vaccinations
        .filter(
            next_due_on__isnull=False,
            next_due_on__gte=today,
        )
        .order_by("next_due_on")
    )

    unscheduled_vaccinations = (
        all_vaccinations
        .filter(next_due_on__isnull=True)
        .order_by("-administered_on")
    )

    pets = (
        Pet.objects
        .filter(owner=request.user)
        .order_by("name")
    )

    context = {
        "today": today,

        "pets": pets,

        "overdue_vaccinations": overdue_vaccinations,
        "upcoming_vaccinations": upcoming_vaccinations,
        "unscheduled_vaccinations": unscheduled_vaccinations,

        "overdue_count": overdue_vaccinations.count(),
        "upcoming_count": upcoming_vaccinations.count(),
        "unscheduled_count": unscheduled_vaccinations.count(),

        "vaccination_count": all_vaccinations.count(),
    }

    return render(
        request,
        "health_app/vaccination_overview.html",
        context,
    )

@login_required
def growth_list(request, pet_id):
    pet = get_owned_pet(request, pet_id)

    records = list(
        GrowthRecord.objects
        .filter(pet=pet)
        .order_by("-measured_on", "-growth_id")
    )

    chart_records = list(reversed(records))

    chart_labels = [
        record.measured_on.strftime("%d %b %Y")
        for record in chart_records
    ]

    weight_data = [
        float(record.weight_kg)
        if record.weight_kg is not None
        else None
        for record in chart_records
    ]

    height_data = [
        float(record.height_cm)
        if record.height_cm is not None
        else None
        for record in chart_records
    ]

    latest_record = records[0] if records else None

    context = {
        "pet": pet,
        "records": records,
        "latest_record": latest_record,
        "chart_labels": chart_labels,
        "weight_data": weight_data,
        "height_data": height_data,
    }

    return render(
        request,
        "health_app/growth_list.html",
        context,
    )


@login_required
def growth_add(request, pet_id):
    pet = get_owned_pet(request, pet_id)

    if request.method == "POST":
        form = GrowthRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.pet = pet
            record.save()

            messages.success(
                request,
                f"Growth measurement added for {pet.name}.",
            )

            return redirect(
                "growth_list",
                pet_id=pet.pet_id,
            )

    else:
        form = GrowthRecordForm()

    return render(
        request,
        "health_app/growth_form.html",
        {
            "pet": pet,
            "form": form,
            "page_title": "Add growth measurement",
            "button_text": "Save measurement",
        },
    )


@login_required
def growth_edit(request, pet_id, growth_id):
    pet = get_owned_pet(request, pet_id)

    record = get_object_or_404(
        GrowthRecord,
        growth_id=growth_id,
        pet=pet,
    )

    if request.method == "POST":
        form = GrowthRecordForm(
            request.POST,
            instance=record,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Growth measurement updated.",
            )

            return redirect(
                "growth_list",
                pet_id=pet.pet_id,
            )

    else:
        form = GrowthRecordForm(instance=record)

    return render(
        request,
        "health_app/growth_form.html",
        {
            "pet": pet,
            "record": record,
            "form": form,
            "page_title": "Edit growth measurement",
            "button_text": "Save changes",
        },
    )


@login_required
def growth_delete(request, pet_id, growth_id):
    pet = get_owned_pet(request, pet_id)

    record = get_object_or_404(
        GrowthRecord,
        growth_id=growth_id,
        pet=pet,
    )

    if request.method == "POST":
        record.delete()

        messages.success(
            request,
            "Growth measurement deleted.",
        )

        return redirect(
            "growth_list",
            pet_id=pet.pet_id,
        )

    return render(
        request,
        "health_app/growth_delete.html",
        {
            "pet": pet,
            "record": record,
        },
    )

@login_required
def reminder_list(request, pet_id):
    pet = get_owned_pet(request, pet_id)

    reminders = (
        CareReminder.objects
        .filter(pet=pet)
        .order_by("remind_at")
    )

    return render(
        request,
        "health_app/reminder_list.html",
        {
            "pet": pet,
            "reminders": reminders,
            "now": timezone.now(),
        },
    )


@login_required
def reminder_add(request, pet_id):
    pet = get_owned_pet(request, pet_id)

    if request.method == "POST":
        form = CareReminderForm(request.POST)

        if form.is_valid():
            reminder = form.save(commit=False)

            reminder.pet = pet
            reminder.status = CareReminder.Status.PENDING
            reminder.completed_at = None

            reminder.save()

            messages.success(
                request,
                f"Reminder added for {pet.name}.",
            )

            return redirect(
                "reminder_list",
                pet_id=pet.pet_id,
            )

    else:
        form = CareReminderForm()

    return render(
        request,
        "health_app/reminder_form.html",
        {
            "pet": pet,
            "form": form,
            "page_title": "Add reminder",
            "button_text": "Save reminder",
        },
    )


@login_required
def reminder_edit(request, pet_id, reminder_id):
    pet = get_owned_pet(request, pet_id)

    reminder = get_object_or_404(
        CareReminder,
        reminder_id=reminder_id,
        pet=pet,
    )

    if request.method == "POST":
        form = CareReminderForm(
            request.POST,
            instance=reminder,
        )

        if form.is_valid():
            reminder = form.save(commit=False)

            # Allow a new notification after editing the reminder.
            reminder.notification_sent_at = None

            reminder.save()

            messages.success(
                request,
                "Reminder updated successfully.",
            )

            return redirect(
                "reminder_list",
                pet_id=pet.pet_id,
            )

    else:
        form = CareReminderForm(instance=reminder)

    return render(
        request,
        "health_app/reminder_form.html",
        {
            "pet": pet,
            "reminder": reminder,
            "form": form,
            "page_title": "Edit reminder",
            "button_text": "Save changes",
        },
    )


@login_required
def reminder_complete(request, pet_id, reminder_id):
    pet = get_owned_pet(request, pet_id)

    reminder = get_object_or_404(
        CareReminder,
        reminder_id=reminder_id,
        pet=pet,
    )

    if request.method == "POST":
        reminder.status = CareReminder.Status.COMPLETED
        reminder.completed_at = timezone.now()

        reminder.save(
            update_fields=[
                "status",
                "completed_at",
            ]
        )

        messages.success(
            request,
            f'"{reminder.title}" marked as completed.',
        )

    return redirect(
        "reminder_list",
        pet_id=pet.pet_id,
    )


@login_required
def reminder_cancel(request, pet_id, reminder_id):
    pet = get_owned_pet(request, pet_id)

    reminder = get_object_or_404(
        CareReminder,
        reminder_id=reminder_id,
        pet=pet,
    )

    if request.method == "POST":
        reminder.status = CareReminder.Status.CANCELLED
        reminder.completed_at = None

        reminder.save(
            update_fields=[
                "status",
                "completed_at",
            ]
        )

        messages.success(
            request,
            "Reminder cancelled.",
        )

    return redirect(
        "reminder_list",
        pet_id=pet.pet_id,
    )


@login_required
def reminder_reopen(request, pet_id, reminder_id):

    pet = get_owned_pet(
        request,
        pet_id,
    )

    reminder = get_object_or_404(
        CareReminder,
        reminder_id=reminder_id,
        pet=pet,
    )

    if request.method == "POST":

        reminder.status = CareReminder.Status.PENDING
        reminder.completed_at = None

        # Allow a new push notification after reopening.
        reminder.notification_sent_at = None

        reminder.save(
            update_fields=[
                "status",
                "completed_at",
                "notification_sent_at",
            ]
        )

        messages.success(
            request,
            "Reminder reopened.",
        )

    return redirect(
        "reminder_list",
        pet_id=pet.pet_id,
    )


@login_required
def reminder_delete(request, pet_id, reminder_id):
    pet = get_owned_pet(request, pet_id)

    reminder = get_object_or_404(
        CareReminder,
        reminder_id=reminder_id,
        pet=pet,
    )

    if request.method == "POST":
        reminder.delete()

        messages.success(
            request,
            "Reminder deleted.",
        )

        return redirect(
            "reminder_list",
            pet_id=pet.pet_id,
        )

    return render(
        request,
        "health_app/reminder_delete.html",
        {
            "pet": pet,
            "reminder": reminder,
        },
    )

@login_required
def reminder_overview(request):
    now = timezone.now()

    reminders = (
        CareReminder.objects
        .filter(pet__owner=request.user)
        .select_related("pet")
    )

    overdue = (
        reminders
        .filter(
            status=CareReminder.Status.PENDING,
            remind_at__lt=now,
        )
        .order_by("remind_at")
    )

    upcoming = (
        reminders
        .filter(
            status=CareReminder.Status.PENDING,
            remind_at__gte=now,
        )
        .order_by("remind_at")
    )

    completed = (
        reminders
        .filter(
            status=CareReminder.Status.COMPLETED,
        )
        .order_by("-completed_at")[:10]
    )

    pets = Pet.objects.filter(
        owner=request.user
    ).order_by("name")

    return render(
        request,
        "health_app/reminder_overview.html",
        {
            "pets": pets,
            "overdue": overdue,
            "upcoming": upcoming,
            "completed": completed,
            "overdue_count": overdue.count(),
            "upcoming_count": upcoming.count(),
        },
    )

@login_required
def notification_settings(request):

    return render(
        request,
        "health_app/notification_settings.html",
        {
            "firebase_api_key":
                settings.FIREBASE_API_KEY,

            "firebase_auth_domain":
                settings.FIREBASE_AUTH_DOMAIN,

            "firebase_project_id":
                settings.FIREBASE_PROJECT_ID,

            "firebase_storage_bucket":
                settings.FIREBASE_STORAGE_BUCKET,

            "firebase_messaging_sender_id":
                settings.FIREBASE_MESSAGING_SENDER_ID,

            "firebase_app_id":
                settings.FIREBASE_APP_ID,

            "firebase_vapid_key":
                settings.FIREBASE_VAPID_KEY,
        },
    )

@login_required
@require_POST
def register_push_device(request):

    try:

        data = json.loads(
            request.body.decode("utf-8")
        )

    except (json.JSONDecodeError, UnicodeDecodeError):

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request."
            },
            status=400,
        )


    fid = str(
        data.get("fid", "")
    ).strip()


    device_name = str(
        data.get(
            "device_name",
            "Web browser"
        )
    ).strip()[:120]


    if not fid:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Firebase Installation ID "
                    "was not provided."
                ),
            },
            status=400,
        )


    device, created = (
        PushDevice.objects.update_or_create(

            firebase_fid=fid,

            defaults={
                "user": request.user,
                "device_name": device_name,
                "is_active": True,
                "last_registered_at":
                    timezone.now(),
            },
        )
        
    )

    request.session["push_fid"] = fid
    return JsonResponse(
        {
            "success": True,
            "created": created,
        }
    )

@login_required
@require_POST
def unregister_push_device(request):

    try:

        data = json.loads(
            request.body.decode("utf-8")
        )

    except (json.JSONDecodeError, UnicodeDecodeError):

        return JsonResponse(
            {
                "success": False
            },
            status=400,
        )


    fid = str(
        data.get("fid", "")
    ).strip()


    if fid:

        PushDevice.objects.filter(
            user=request.user,
            firebase_fid=fid,
        ).update(
            is_active=False
        )


    return JsonResponse(
        {
            "success": True
        }
    )

def firebase_messaging_service_worker(request):

    return render(
        request,
        "firebase-messaging-sw.js",
        {
            "firebase_api_key":
                settings.FIREBASE_API_KEY,

            "firebase_auth_domain":
                settings.FIREBASE_AUTH_DOMAIN,

            "firebase_project_id":
                settings.FIREBASE_PROJECT_ID,

            "firebase_storage_bucket":
                settings.FIREBASE_STORAGE_BUCKET,

            "firebase_messaging_sender_id":
                settings.FIREBASE_MESSAGING_SENDER_ID,

            "firebase_app_id":
                settings.FIREBASE_APP_ID,
        },

        content_type="application/javascript",
    )


@login_required
@ensure_csrf_cookie
def notification_settings(request):

    return render(
        request,
        "health_app/notification_settings.html",
        {
            "firebase_api_key":
                settings.FIREBASE_API_KEY,

            "firebase_auth_domain":
                settings.FIREBASE_AUTH_DOMAIN,

            "firebase_project_id":
                settings.FIREBASE_PROJECT_ID,

            "firebase_storage_bucket":
                settings.FIREBASE_STORAGE_BUCKET,

            "firebase_messaging_sender_id":
                settings.FIREBASE_MESSAGING_SENDER_ID,

            "firebase_app_id":
                settings.FIREBASE_APP_ID,

            "firebase_vapid_key":
                settings.FIREBASE_VAPID_KEY,
        },
    )

@csrf_exempt
@require_POST
def run_reminder_pushes(request):

    expected_secret = os.getenv(
        "REMINDER_CRON_SECRET",
        "",
    )

    if not expected_secret:
        return JsonResponse(
            {
                "success": False,
                "message": "Cron secret is not configured.",
            },
            status=503,
        )

    authorization = request.headers.get(
        "Authorization",
        "",
    )

    prefix = "Bearer "

    if not authorization.startswith(prefix):
        return JsonResponse(
            {
                "success": False,
                "message": "Unauthorized.",
            },
            status=401,
        )

    provided_secret = authorization[
        len(prefix):
    ].strip()

    if not secrets.compare_digest(
        provided_secret,
        expected_secret,
    ):
        return JsonResponse(
            {
                "success": False,
                "message": "Unauthorized.",
            },
            status=401,
        )

    output = StringIO()

    try:

        call_command(
            "send_reminder_pushes",
            stdout=output,
        )

    except Exception as exc:

        print(
            "Reminder cron failed:",
            repr(exc),
        )

        return JsonResponse(
            {
                "success": False,
                "message": "Reminder processing failed.",
            },
            status=500,
        )

    return JsonResponse(
        {
            "success": True,
            "message": "Reminder check completed.",
        }
    )