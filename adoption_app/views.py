from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone

from .forms import AdoptionListingForm
from .models import AdoptionListing


@login_required
def adoption_browse(request):

    search = request.GET.get(
        "q",
        "",
    ).strip()

    listings = (
        AdoptionListing.objects
        .filter(
            listing_status=
            AdoptionListing.ListingStatus.ACTIVE
        )
        .select_related(
            "pet",
            "pet__owner",
        )
    )

    if search:
        listings = listings.filter(
            Q(pet__name__icontains=search)
            | Q(pet__species__icontains=search)
            | Q(pet__breed__icontains=search)
            | Q(location__icontains=search)
            | Q(description__icontains=search)
        )

    return render(
        request,
        "adoption_app/adoption_browse.html",
        {
            "listings": listings,
            "search": search,
        },
    )


@login_required
def my_adoption_listings(request):

    listings = (
        AdoptionListing.objects
        .filter(
            pet__owner=request.user
        )
        .select_related("pet")
        .order_by(
            "-listed_at",
            "-listing_id",
        )
    )

    return render(
        request,
        "adoption_app/my_listings.html",
        {
            "listings": listings,
        },
    )


@login_required
def adoption_create(request):

    if request.method == "POST":

        form = AdoptionListingForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            listing = form.save(
                commit=False
            )

            listing.listing_status = (
                AdoptionListing.ListingStatus.ACTIVE
            )

            listing.listed_at = timezone.now()
            listing.closed_at = None

            listing.save()

            messages.success(
                request,
                f"{listing.pet.name} is now listed for adoption.",
            )

            return redirect(
                "adoption_detail",
                listing_id=listing.listing_id,
            )

    else:

        form = AdoptionListingForm(
            user=request.user
        )

    return render(
        request,
        "adoption_app/adoption_form.html",
        {
            "form": form,
            "page_title": "Create adoption listing",
            "button_text": "Publish listing",
        },
    )


@login_required
def adoption_detail(request, listing_id):

    listing = get_object_or_404(
        AdoptionListing.objects.select_related(
            "pet",
            "pet__owner",
        ),
        listing_id=listing_id,
    )

    return render(
        request,
        "adoption_app/adoption_detail.html",
        {
            "listing": listing,
        },
    )


@login_required
def adoption_edit(request, listing_id):

    listing = get_object_or_404(
        AdoptionListing,
        listing_id=listing_id,
        pet__owner=request.user,
    )

    if request.method == "POST":

        form = AdoptionListingForm(
            request.POST,
            user=request.user,
            instance=listing,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Adoption listing updated.",
            )

            return redirect(
                "adoption_detail",
                listing_id=listing.listing_id,
            )

    else:

        form = AdoptionListingForm(
            user=request.user,
            instance=listing,
        )

    return render(
        request,
        "adoption_app/adoption_form.html",
        {
            "form": form,
            "listing": listing,
            "page_title": "Edit adoption listing",
            "button_text": "Save changes",
        },
    )


@login_required
def adoption_mark_adopted(
    request,
    listing_id,
):

    listing = get_object_or_404(
        AdoptionListing,
        listing_id=listing_id,
        pet__owner=request.user,
    )

    if request.method == "POST":

        listing.listing_status = (
            AdoptionListing.ListingStatus.ADOPTED
        )

        listing.closed_at = timezone.now()

        listing.save(
            update_fields=[
                "listing_status",
                "closed_at",
            ]
        )

        messages.success(
            request,
            f"{listing.pet.name} has been marked as adopted.",
        )

    return redirect(
        "adoption_detail",
        listing_id=listing.listing_id,
    )


@login_required
def adoption_close(
    request,
    listing_id,
):

    listing = get_object_or_404(
        AdoptionListing,
        listing_id=listing_id,
        pet__owner=request.user,
    )

    if request.method == "POST":

        listing.listing_status = (
            AdoptionListing.ListingStatus.CLOSED
        )

        listing.closed_at = timezone.now()

        listing.save(
            update_fields=[
                "listing_status",
                "closed_at",
            ]
        )

        messages.success(
            request,
            "Adoption listing closed.",
        )

    return redirect(
        "adoption_detail",
        listing_id=listing.listing_id,
    )


@login_required
def adoption_reopen(
    request,
    listing_id,
):

    listing = get_object_or_404(
        AdoptionListing,
        listing_id=listing_id,
        pet__owner=request.user,
    )

    if request.method == "POST":

        active_exists = (
            AdoptionListing.objects
            .filter(
                pet=listing.pet,
                listing_status=
                AdoptionListing.ListingStatus.ACTIVE,
            )
            .exclude(
                listing_id=listing.listing_id
            )
            .exists()
        )

        if active_exists:

            messages.error(
                request,
                (
                    "This pet already has another active "
                    "adoption listing."
                ),
            )

        else:

            listing.listing_status = (
                AdoptionListing.ListingStatus.ACTIVE
            )

            listing.closed_at = None
            listing.listed_at = timezone.now()

            listing.save(
                update_fields=[
                    "listing_status",
                    "closed_at",
                    "listed_at",
                ]
            )

            messages.success(
                request,
                "Adoption listing reopened.",
            )

    return redirect(
        "adoption_detail",
        listing_id=listing.listing_id,
    )
