from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.community_feed,
        name="community_feed",
    ),

    path(
        "mine/",
        views.my_posts,
        name="my_community_posts",
    ),

    path(
        "create/",
        views.post_create,
        name="community_post_create",
    ),

    
    path(
    "admin/<int:post_id>/approve/",
    views.admin_post_approve,
    name="community_post_approve",
    ),

    path(
        "admin/<int:post_id>/reject/",
        views.admin_post_reject,
        name="community_post_reject",
    ),
    path(
            "<int:post_id>/",
            views.post_detail,
            name="community_post_detail",
    ),

    path(
        "<int:post_id>/edit/",
        views.post_edit,
        name="community_post_edit",
    ),

    path(
        "<int:post_id>/delete/",
        views.post_delete,
        name="community_post_delete",
    ),

    path(
        "<int:post_id>/comments/add/",
        views.comment_add,
        name="community_comment_add",
    ),

    path(
        "<int:post_id>/comments/<int:comment_id>/delete/",
        views.comment_delete,
        name="community_comment_delete",
    ),

]