from django.conf import settings
from django.db import models


class CommunityPost(models.Model):

    class ModerationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    post_id = models.BigAutoField(primary_key=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="author_id",
        related_name="community_posts",
    )

    title = models.CharField(
        max_length=255,
    )

    body = models.TextField()

    image = models.ImageField(
        upload_to="community/",
        db_column="image_url",
        max_length=500,
        blank=True,
        null=True,
    )

    moderation_status = models.CharField(
        max_length=20,
        choices=ModerationStatus.choices,
        default=ModerationStatus.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "community_posts"
        managed = False
        ordering = [
            "-created_at",
            "-post_id",
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):

    class ModerationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    comment_id = models.BigAutoField(
        primary_key=True,
    )

    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        db_column="post_id",
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="author_id",
        related_name="community_comments",
    )

    body = models.TextField()

    moderation_status = models.CharField(
        max_length=20,
        choices=ModerationStatus.choices,
        default=ModerationStatus.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "comments"
        managed = False
        ordering = [
            "created_at",
            "comment_id",
        ]

    def __str__(self):
        return f"Comment by {self.author.full_name}"