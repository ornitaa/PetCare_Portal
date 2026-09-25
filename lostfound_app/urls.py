from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.report_overview,
        name="report_overview",
    ),

    path(
        "mine/",
        views.my_reports,
        name="my_reports",
    ),

    path(
        "create/",
        views.report_add,
        name="report_add",
    ),

    path(
        "<int:report_id>/",
        views.report_detail,
        name="report_detail",
    ),

    path(
        "<int:report_id>/edit/",
        views.report_edit,
        name="report_edit",
    ),

    path(
        "<int:report_id>/resolve/",
        views.report_resolve,
        name="report_resolve",
    ),

    path(
        "<int:report_id>/reopen/",
        views.report_reopen,
        name="report_reopen",
    ),

    path(
        "<int:report_id>/delete/",
        views.report_delete,
        name="report_delete",
    ),
]