from django import forms

from .models import PetReport


class PetReportForm(forms.ModelForm):

    class Meta:
        model = PetReport

        fields = (
            "report_type",
            "pet",
            "location",
            "incident_at",
            "description",
            "photo",
        )

        widgets = {
            "report_type": forms.Select(
                attrs={
                    "class": "form-select pet-input",
                    "id": "id_report_type",
                }
            ),

            "pet": forms.Select(
                attrs={
                    "class": "form-select pet-input",
                    "id": "id_pet",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. Dhanmondi, Dhaka",
                }
            ),

            "incident_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "class": "form-control pet-input",
                    "type": "datetime-local",
                },
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 5,
                    "placeholder": (
                        "Describe the pet, circumstances, "
                        "distinctive features and other useful details."
                    ),
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control pet-input",
                    "accept": "image/*",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        self.fields["incident_at"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]

        self.fields["pet"].required = False
        self.fields["pet"].empty_label = (
            "No registered pet selected"
        )

        if user is not None:
            self.fields["pet"].queryset = (
                user.pets.all().order_by("name")
            )
        else:
            self.fields["pet"].queryset = (
                self.fields["pet"].queryset.none()
            )

    def clean(self):
        cleaned = super().clean()

        report_type = cleaned.get("report_type")
        pet = cleaned.get("pet")

        if (
            report_type == PetReport.ReportType.LOST
            and pet is None
        ):
            self.add_error(
                "pet",
                "Select the registered pet that is missing.",
            )

        if (
            pet is not None
            and self.user is not None
            and pet.owner_id != self.user.pk
        ):
            self.add_error(
                "pet",
                "You can only select one of your own pets.",
            )

        return cleaned