from django import forms

from pets_app.models import Pet

from .models import AdoptionListing


class AdoptionListingForm(forms.ModelForm):

    class Meta:
        model = AdoptionListing

        fields = (
            "pet",
            "location",
            "description",
        )

        widgets = {
            "pet": forms.Select(
                attrs={
                    "class": "form-select pet-input",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "e.g. Dhaka, Bangladesh",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 6,
                    "placeholder": (
                        "Describe the pet, personality, care needs, "
                        "and what kind of home would be suitable."
                    ),
                }
            ),
        }

    def __init__(
        self,
        *args,
        user=None,
        instance=None,
        **kwargs,
    ):
        super().__init__(
            *args,
            instance=instance,
            **kwargs,
        )

        self.user = user

        if user is None:
            self.fields["pet"].queryset = Pet.objects.none()
            return

        pets = Pet.objects.filter(
            owner=user
        ).order_by("name")

        # While editing, allow the current listing's pet.
        current_listing_id = (
            instance.listing_id
            if instance and instance.pk
            else None
        )

        active_pet_ids = (
            AdoptionListing.objects
            .filter(
                listing_status=
                AdoptionListing.ListingStatus.ACTIVE
            )
            .exclude(
                listing_id=current_listing_id
            )
            .values_list(
                "pet_id",
                flat=True,
            )
        )

        self.fields["pet"].queryset = (
            pets.exclude(
                pet_id__in=active_pet_ids
            )
        )

    def clean_pet(self):
        pet = self.cleaned_data.get("pet")

        if pet is None:
            return pet

        if (
            self.user is not None
            and pet.owner_id != self.user.pk
        ):
            raise forms.ValidationError(
                "You can only create an adoption listing "
                "for one of your own pets."
            )

        active_listings = AdoptionListing.objects.filter(
            pet=pet,
            listing_status=
            AdoptionListing.ListingStatus.ACTIVE,
        )

        if self.instance and self.instance.pk:
            active_listings = active_listings.exclude(
                listing_id=self.instance.listing_id
            )

        if active_listings.exists():
            raise forms.ValidationError(
                "This pet already has an active adoption listing."
            )

        return pet