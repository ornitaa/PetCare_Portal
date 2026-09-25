from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from .forms import CommentForm, CommunityPostForm
from .models import Comment, CommunityPost


@login_required
def community_feed(request):

    search = request.GET.get(
        "q",
        "",
    ).strip()

    posts = (
        CommunityPost.objects
        .filter(
            moderation_status=
            CommunityPost.ModerationStatus.APPROVED
        )
        .select_related(
            "author"
        )
        .annotate(
            approved_comment_count=Count(
                "comments",
                filter=Q(
                    comments__moderation_status=
                    Comment.ModerationStatus.APPROVED
                ),
            )
        )
    )

    if search:

        posts = posts.filter(
            Q(title__icontains=search)
            | Q(body__icontains=search)
            | Q(author__full_name__icontains=search)
        )

    posts = posts.order_by(
        "-created_at",
        "-post_id",
    )

    return render(
        request,
        "community_app/community_feed.html",
        {
            "posts": posts,
            "search": search,
        },
    )

@login_required
def my_posts(request):

    posts = (
        CommunityPost.objects
        .filter(author=request.user)
        .annotate(
            approved_comment_count=Count(
                "comments",
                filter=Q(
                    comments__moderation_status=
                    Comment.ModerationStatus.APPROVED
                ),
            )
        )
        .order_by(
            "-created_at",
            "-post_id",
        )
    )

    return render(
        request,
        "community_app/my_posts.html",
        {
            "posts": posts,
        },
    )


@login_required
def post_create(request):

    if request.method == "POST":

        form = CommunityPostForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.author = request.user

            post.moderation_status = (
                CommunityPost.ModerationStatus.PENDING
            )

            post.save()

            messages.success(
                request,
                (
                    "Your post was submitted successfully "
                    "and is awaiting approval."
                ),
            )

            return redirect(
                "my_community_posts"
            )

    else:
        form = CommunityPostForm()

    return render(
        request,
        "community_app/post_form.html",
        {
            "form": form,
            "page_title": "Create a post",
            "button_text": "Submit post",
        },
    )


@login_required
def post_detail(request, post_id):

    post = get_object_or_404(
        CommunityPost.objects.select_related(
            "author"
        ),
        post_id=post_id,
    )

    # Public users can only see approved posts.
    # Author can additionally view their own pending/rejected post.
    if (
        post.moderation_status
        != CommunityPost.ModerationStatus.APPROVED
        and post.author_id != request.user.pk
        and not request.user.is_staff
    ):
        return redirect("community_feed")

    comments = (
        Comment.objects
        .filter(
            post=post,
            moderation_status=
            Comment.ModerationStatus.APPROVED,
        )
        .select_related("author")
    )

    comment_form = CommentForm()

    return render(
        request,
        "community_app/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


@login_required
def post_edit(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
        author=request.user,
    )

    if request.method == "POST":

        form = CommunityPostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():

            edited_post = form.save(
                commit=False
            )

            # Edited posts require moderation again.
            edited_post.moderation_status = (
                CommunityPost.ModerationStatus.PENDING
            )

            edited_post.save()

            messages.success(
                request,
                (
                    "Post updated. It has been sent "
                    "for moderation again."
                ),
            )

            return redirect(
                "my_community_posts"
            )

    else:

        form = CommunityPostForm(
            instance=post
        )

    return render(
        request,
        "community_app/post_form.html",
        {
            "form": form,
            "post": post,
            "page_title": "Edit post",
            "button_text": "Save changes",
        },
    )


@login_required
def post_delete(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
        author=request.user,
    )

    if request.method == "POST":

        post.delete()

        messages.success(
            request,
            "Post deleted.",
        )

        return redirect(
            "my_community_posts"
        )

    return render(
        request,
        "community_app/post_delete.html",
        {
            "post": post,
        },
    )


@login_required
def comment_add(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
        moderation_status=
        CommunityPost.ModerationStatus.APPROVED,
    )

    if request.method == "POST":

        form = CommentForm(
            request.POST
        )

        if form.is_valid():

            comment = form.save(
                commit=False
            )

            comment.post = post
            comment.author = request.user

            comment.moderation_status = (
                Comment.ModerationStatus.APPROVED
            )

            comment.save()

            messages.success(
                request,
                (
                    "Your comment was posted successfully."
                ),
            )

    return redirect(
        "community_post_detail",
        post_id=post.post_id,
    )


@login_required
def comment_delete(
    request,
    post_id,
    comment_id,
):

    comment = get_object_or_404(
        Comment,
        comment_id=comment_id,
        post_id=post_id,
        author=request.user,
    )

    post_id = comment.post_id

    if request.method == "POST":

        comment.delete()

        messages.success(
            request,
            "Comment deleted.",
        )

    return redirect(
        "community_post_detail",
        post_id=post_id,
    )
# ============================================================
# ADMIN - APPROVE COMMUNITY POST
# ============================================================

@staff_member_required(login_url="login")
@require_POST
def admin_post_approve(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
    )

    post.moderation_status = (
        CommunityPost.ModerationStatus.APPROVED
    )

    post.save(
        update_fields=[
            "moderation_status",
        ]
    )

    messages.success(
        request,
        f'"{post.title}" has been approved.',
    )

    return redirect(
        "admin_dashboard"
    )


# ============================================================
# ADMIN - REJECT COMMUNITY POST
# ============================================================

@staff_member_required(login_url="login")
@require_POST
def admin_post_reject(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
    )

    post.moderation_status = (
        CommunityPost.ModerationStatus.REJECTED
    )

    post.save(
        update_fields=[
            "moderation_status",
        ]
    )

    messages.success(
        request,
        f'"{post.title}" has been rejected.',
    )

    return redirect(
        "admin_dashboard"
    )