from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PetForm
from .models import Pet


@login_required
def pet_list(request):

    pets = Pet.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    return render(
        request,
        "pets_app/pet_list.html",
        {
            "pets": pets,
        },
    )


@login_required
def pet_add(request):

    if request.method == "POST":

        form = PetForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            pet = form.save(commit=False)

            pet.owner = request.user

            pet.save()

            messages.success(
                request,
                f"{pet.name}'s profile has been created.",
            )

            return redirect(
                "pet_detail",
                pet_id=pet.pet_id,
            )

    else:
        form = PetForm()

    return render(
        request,
        "pets_app/pet_form.html",
        {
            "form": form,
            "page_title": "Add a pet",
            "button_text": "Create pet profile",
        },
    )


@login_required
def pet_detail(request, pet_id):

    pet = get_object_or_404(
        Pet,
        pet_id=pet_id,
        owner=request.user,
    )

    return render(
        request,
        "pets_app/pet_detail.html",
        {
            "pet": pet,
        },
    )


@login_required
def pet_edit(request, pet_id):

    pet = get_object_or_404(
        Pet,
        pet_id=pet_id,
        owner=request.user,
    )

    if request.method == "POST":

        form = PetForm(
            request.POST,
            request.FILES,
            instance=pet,
        )

        if form.is_valid():

            pet = form.save()

            messages.success(
                request,
                f"{pet.name}'s profile has been updated.",
            )

            return redirect(
                "pet_detail",
                pet_id=pet.pet_id,
            )

    else:

        form = PetForm(
            instance=pet,
        )

    return render(
        request,
        "pets_app/pet_form.html",
        {
            "form": form,
            "pet": pet,
            "page_title": "Edit pet",
            "button_text": "Save changes",
        },
    )


@login_required
def pet_delete(request, pet_id):

    pet = get_object_or_404(
        Pet,
        pet_id=pet_id,
        owner=request.user,
    )

    if request.method == "POST":

        pet_name = pet.name

        pet.delete()

        messages.success(
            request,
            f"{pet_name}'s profile has been deleted.",
        )

        return redirect("pet_list")

    return render(
        request,
        "pets_app/pet_confirm_delete.html",
        {
            "pet": pet,
        },
    )
