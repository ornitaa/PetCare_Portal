from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.nearby_vets,
        name="nearby_vets",
    ),
]