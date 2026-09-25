from django.urls import include, path

from . import views


urlpatterns = [

    path(
        "",
        views.pet_list,
        name="pet_list",
    ),

    path(
        "add/",
        views.pet_add,
        name="pet_add",
    ),

    # Health module
    path(
        "<int:pet_id>/health/",
        include("health_app.urls"),
    ),

    path(
        "<int:pet_id>/edit/",
        views.pet_edit,
        name="pet_edit",
    ),

    path(
        "<int:pet_id>/delete/",
        views.pet_delete,
        name="pet_delete",
    ),

    path(
        "<int:pet_id>/",
        views.pet_detail,
        name="pet_detail",
    ),
]