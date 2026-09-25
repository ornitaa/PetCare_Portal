from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, RegisterForm, ProfileUpdateForm
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model

from pets_app.models import Pet

from health_app.models import Vaccination, CareReminder
from community_app.models import CommunityPost
from adoption_app.models import AdoptionListing
User = get_user_model()

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(
        request,
        "users_app/home.html",
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Welcome to PetCare! Your account has been created.",
            )

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "users_app/register.html",
        {
            "form": form,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data["remember_me"]

            user = authenticate(
                request,
                email=email,
                password=password,
            )

            if user is not None:
                login(request, user)

                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    request.session.set_expiry(0)

                messages.success(
                    request,
                    f"Welcome back, {user.full_name}!",
                )

                next_url = request.GET.get("next")

                if (
                    next_url
                    and url_has_allowed_host_and_scheme(
                        url=next_url,
                        allowed_hosts={request.get_host()},
                        require_https=request.is_secure(),
                    )
                ):
                    return redirect(next_url)

                return redirect("dashboard")

            form.add_error(
                None,
                "We couldn't sign you in with that email and password.",
            )

    else:
        form = LoginForm()

    return render(
        request,
        "users_app/login.html",
        {
            "form": form,
        },
    )


@login_required
def logout_view(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully.",
    )

    return redirect("login")


@login_required
def dashboard(request):

    pets_queryset = request.user.pets.all()

    upcoming_vaccine_count = (
        Vaccination.objects
        .filter(
            pet__owner=request.user,
            next_due_on__isnull=False,
            next_due_on__gte=date.today(),
        )
        .count()
    )

    care_reminder_count = (
        CareReminder.objects
        .filter(
            pet__owner=request.user,
            status=CareReminder.Status.PENDING,
        )
        .count()
    )

    my_post_count = (
        CommunityPost.objects
        .filter(author=request.user)
        .count()
    )

    # Latest approved community discussions
    latest_community_posts = (
        CommunityPost.objects
        .filter(
            moderation_status=
            CommunityPost.ModerationStatus.APPROVED
        )
        .select_related("author")
        .order_by("-created_at")[:3]
    )

    # Latest active adoption listings
    latest_adoption_listings = (
        AdoptionListing.objects
        .filter(
            listing_status=
            AdoptionListing.ListingStatus.ACTIVE
        )
        .select_related(
            "pet",
            "pet__owner",
        )
        .order_by("-listed_at")[:3]
    )

    context = {
        "pets": pets_queryset[:4],
        "pet_count": pets_queryset.count(),

        "upcoming_vaccine_count": upcoming_vaccine_count,
        "care_reminder_count": care_reminder_count,
        "my_post_count": my_post_count,

        "latest_community_posts": latest_community_posts,
        "latest_adoption_listings": latest_adoption_listings,
    }

    return render(
        request,
        "users_app/dashboard.html",
        context,
    )

@login_required
def account_profile(request):

    pet_count = request.user.pets.count()

    post_count = (
        CommunityPost.objects
        .filter(author=request.user)
        .count()
    )

    active_adoption_count = (
        AdoptionListing.objects
        .filter(
            pet__owner=request.user,
            listing_status=AdoptionListing.ListingStatus.ACTIVE,
        )
        .count()
    )

    pending_reminder_count = (
        CareReminder.objects
        .filter(
            pet__owner=request.user,
            status=CareReminder.Status.PENDING,
        )
        .count()
    )

    context = {
        "pet_count": pet_count,
        "post_count": post_count,
        "active_adoption_count": active_adoption_count,
        "pending_reminder_count": pending_reminder_count,
    }

    return render(
        request,
        "users_app/account_profile.html",
        context,
    )

@login_required
def account_edit(request):

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully.",
            )

            return redirect(
                "account_profile"
            )

    else:

        form = ProfileUpdateForm(
            instance=request.user,
        )

    return render(
        request,
        "users_app/account_edit.html",
        {
            "form": form,
        },
    )

@login_required
def emergency_guide(request):

    return render(
        request,
        "users_app/emergency_guide.html",
    )
@staff_member_required(login_url="login")
def admin_dashboard(request):

    today = date.today()

    # =========================================================
    # MAIN STATISTICS
    # =========================================================

    total_users = (
        User.objects
        .filter(is_staff=False)
        .count()
    )

    total_pets = Pet.objects.count()

    total_posts = CommunityPost.objects.count()

    pending_post_count = (
        CommunityPost.objects
        .filter(
            moderation_status=
            CommunityPost.ModerationStatus.PENDING
        )
        .count()
    )

    active_adoption_count = (
        AdoptionListing.objects
        .filter(
            listing_status=
            AdoptionListing.ListingStatus.ACTIVE
        )
        .count()
    )

    total_vaccinations = Vaccination.objects.count()

    upcoming_vaccination_count = (
        Vaccination.objects
        .filter(
            next_due_on__isnull=False,
            next_due_on__gte=today,
        )
        .count()
    )

    pending_reminder_count = (
        CareReminder.objects
        .filter(
            status=CareReminder.Status.PENDING
        )
        .count()
    )


    # =========================================================
    # RECENT USERS
    # =========================================================

    recent_users = (
        User.objects
        .filter(is_staff=False)
        .order_by("-created_at")[:5]
    )


    # =========================================================
    # PENDING COMMUNITY POSTS
    # =========================================================

    pending_posts = (
        CommunityPost.objects
        .filter(
            moderation_status=
            CommunityPost.ModerationStatus.PENDING
        )
        .select_related("author")
        .order_by("-created_at")[:5]
    )


    # =========================================================
    # RECENT ADOPTION LISTINGS
    # =========================================================

    recent_adoptions = (
        AdoptionListing.objects
        .select_related(
            "pet",
            "pet__owner",
        )
        .order_by("-listed_at")[:5]
    )


    context = {
        "total_users": total_users,
        "total_pets": total_pets,
        "total_posts": total_posts,
        "pending_post_count": pending_post_count,

        "active_adoption_count":
            active_adoption_count,

        "total_vaccinations":
            total_vaccinations,

        "upcoming_vaccination_count":
            upcoming_vaccination_count,

        "pending_reminder_count":
            pending_reminder_count,

        "recent_users": recent_users,
        "pending_posts": pending_posts,
        "recent_adoptions": recent_adoptions,
    }

    return render(
        request,
        "users_app/admin_dashboard.html",
        context,
    )