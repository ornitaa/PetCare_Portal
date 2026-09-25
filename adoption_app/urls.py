from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.adoption_browse,
        name="adoption_browse",
    ),

    path(
        "mine/",
        views.my_adoption_listings,
        name="my_adoption_listings",
    ),

    path(
        "create/",
        views.adoption_create,
        name="adoption_create",
    ),

    path(
        "<int:listing_id>/",
        views.adoption_detail,
        name="adoption_detail",
    ),

    path(
        "<int:listing_id>/edit/",
        views.adoption_edit,
        name="adoption_edit",
    ),

    path(
        "<int:listing_id>/adopted/",
        views.adoption_mark_adopted,
        name="adoption_mark_adopted",
    ),

    path(
        "<int:listing_id>/close/",
        views.adoption_close,
        name="adoption_close",
    ),

    path(
        "<int:listing_id>/reopen/",
        views.adoption_reopen,
        name="adoption_reopen",
    ),

]