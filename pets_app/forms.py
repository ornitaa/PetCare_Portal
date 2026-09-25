from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Pet


class PetForm(forms.ModelForm):

    class Meta:
        model = Pet

        fields = (
            "name",
            "species",
            "breed",
            "sex",
            "birth_date",
            "photo",
        )

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": _("Pet's name"),
                }
            ),

            "species": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": _("e.g. Cat, Dog"),
                }
            ),

            "breed": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": _("Breed (optional)"),
                }
            ),

            "sex": forms.Select(
                attrs={
                    "class": "form-select pet-input",
                }
            ),

            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control pet-input",
                    "type": "date",
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control pet-input",
                    "accept": "image/*",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Translate the labels shown inside the sex dropdown.
        self.fields["sex"].choices = [
            (
                value,
                _(str(label)),
            )
            for value, label in self.fields["sex"].choices
        ]