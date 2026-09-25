from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def nearby_vets(request):
    return render(
        request,
        "vets_app/nearby_vets.html",
        {
            "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        },
    )