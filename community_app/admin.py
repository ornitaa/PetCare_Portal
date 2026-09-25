from django.contrib import admin

from .models import Comment, CommunityPost


@admin.action(description="Approve selected posts")
def approve_posts(modeladmin, request, queryset):
    queryset.update(
        moderation_status=
        CommunityPost.ModerationStatus.APPROVED
    )


@admin.action(description="Reject selected posts")
def reject_posts(modeladmin, request, queryset):
    queryset.update(
        moderation_status=
        CommunityPost.ModerationStatus.REJECTED
    )


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):

    list_display = (
        "post_id",
        "title",
        "author",
        "moderation_status",
        "created_at",
    )

    list_filter = (
        "moderation_status",
        "created_at",
    )

    search_fields = (
        "title",
        "body",
        "author__full_name",
        "author__email",
    )

    actions = (
        approve_posts,
        reject_posts,
    )



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "comment_id",
        "post",
        "author",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "body",
        "author__full_name",
        "post__title",
    )