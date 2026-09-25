from datetime import date

from django import forms

from .models import MedicalRecord, Medication, Vaccination, GrowthRecord, CareReminder


class MedicalRecordForm(forms.ModelForm):

    class Meta:
        model = MedicalRecord

        fields = (
            "recorded_on",
            "record_kind",
            "diagnosis",
            "care_notes",
            "vet_name",
            "attachment",
        )

        widgets = {
            "recorded_on": forms.DateInput(
                attrs={
                    "class": "form-control pet-input",
                    "type": "date",
                }
            ),

            "record_kind": forms.Select(
                attrs={
                    "class": "form-select pet-input",
                }
            ),

            "diagnosis": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 3,
                    "placeholder": "Diagnosis or health condition",
                }
            ),

            "care_notes": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 4,
                    "placeholder": "Treatment, observations or care instructions",
                }
            ),

            "vet_name": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "Veterinarian name (optional)",
                }
            ),

            "attachment": forms.ClearableFileInput(
                attrs={
                    "class": "form-control pet-input",
                    "accept": ".pdf,.jpg,.jpeg,.png",
                }
            ),
        }

    def clean_recorded_on(self):
        value = self.cleaned_data["recorded_on"]

        if value > date.today():
            raise forms.ValidationError(
                "Medical record date cannot be in the future."
            )

        return value


class MedicationForm(forms.ModelForm):

    class Meta:
        model = Medication

        fields = (
            "medication_name",
            "dose",
            "route",
            "frequency",
            "start_date",
            "end_date",
            "notes",
        )

        widgets = {
            "medication_name": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "Medication name",
                }
            ),

            "dose": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. 2.5 ml",
                }
            ),

            "route": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. Oral",
                }
            ),

            "frequency": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. Twice daily",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control pet-input",
                    "type": "date",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control pet-input",
                    "type": "date",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 3,
                    "placeholder": "Optional medication instructions",
                }
            ),
        }

    def clean(self):
        cleaned = super().clean()

        start = cleaned.get("start_date")
        end = cleaned.get("end_date")

        if start and end and end < start:
            self.add_error(
                "end_date",
                "End date cannot be before the start date.",
            )

        return cleaned

class VaccinationForm(forms.ModelForm):

    class Meta:
        model = Vaccination

        fields = (
            "vaccine_name",
            "dose_label",
            "administered_on",
            "next_due_on",
            "clinic_name",
            "notes",
        )

        widgets = {
            "vaccine_name": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. Rabies",
                }
            ),

            "dose_label": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. Booster / Dose 1",
                }
            ),

            "administered_on": forms.DateInput(
                attrs={
                    "class": "form-control pet-input",
                    "type": "date",
                }
            ),

            "next_due_on": forms.DateInput(
                attrs={
                    "class": "form-control pet-input",
                    "type": "date",
                }
            ),

            "clinic_name": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "Veterinary clinic (optional)",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 3,
                    "placeholder": "Optional notes",
                }
            ),
        }

    def clean_administered_on(self):
        value = self.cleaned_data["administered_on"]

        if value > date.today():
            raise forms.ValidationError(
                "Administration date cannot be in the future."
            )

        return value

    def clean(self):
        cleaned = super().clean()

        administered = cleaned.get("administered_on")
        next_due = cleaned.get("next_due_on")

        if (
            administered
            and next_due
            and next_due < administered
        ):
            self.add_error(
                "next_due_on",
                "Next due date cannot be before the administration date.",
            )

        return cleaned

class GrowthRecordForm(forms.ModelForm):

    class Meta:
        model = GrowthRecord

        fields = (
            "measured_on",
            "weight_kg",
            "height_cm",
            "milestone",
            "notes",
        )

        widgets = {
            "measured_on": forms.DateInput(
                attrs={
                    "class": "form-control pet-input",
                    "type": "date",
                }
            ),

            "weight_kg": forms.NumberInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. 4.50",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),

            "height_cm": forms.NumberInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. 32.5",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),

            "milestone": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. Reached adult weight",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 3,
                    "placeholder": "Optional notes about growth or development",
                }
            ),
        }

    def clean_measured_on(self):
        value = self.cleaned_data["measured_on"]

        if value > date.today():
            raise forms.ValidationError(
                "Measurement date cannot be in the future."
            )

        return value

    def clean(self):
        cleaned = super().clean()

        weight = cleaned.get("weight_kg")
        height = cleaned.get("height_cm")

        if weight is None and height is None:
            raise forms.ValidationError(
                "Enter at least a weight or height measurement."
            )

        return cleaned

class CareReminderForm(forms.ModelForm):

    class Meta:
        model = CareReminder

        fields = (
            "title",
            "reminder_kind",
            "remind_at",
            "details",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. Annual vet checkup",
                }
            ),

            "reminder_kind": forms.Select(
                attrs={
                    "class": "form-select pet-input",
                }
            ),

            "remind_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "class": "form-control pet-input",
                    "type": "datetime-local",
                },
            ),

            "details": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 4,
                    "placeholder": "Optional instructions or notes",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["remind_at"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]