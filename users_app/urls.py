from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.urls import path, reverse_lazy


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "register/",
        views.register_view,
        name="register",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
    path(
    "account/",
    views.account_profile,
    name="account_profile",
    ),
    path(
    "account/edit/",
    views.account_edit,
    name="account_edit",
    ),
    
    path(
    "account/change-password/",
    auth_views.PasswordChangeView.as_view(
        template_name="users_app/password_change.html",
        success_url="/account/password-changed/",
    ),
    name="password_change",
    ),
    path(
    "account/password-changed/",
    auth_views.PasswordChangeDoneView.as_view(
        template_name="users_app/password_change_done.html",
    ),
    name="password_change_done",
    ),
    path(
    "account/change-password/",
    auth_views.PasswordChangeView.as_view(
        template_name="users_app/password_change.html",
        success_url=reverse_lazy("password_change_done"),
    ),
    name="password_change",
),

path(
    "account/password-changed/",
    auth_views.PasswordChangeDoneView.as_view(
        template_name="users_app/password_change_done.html",
    ),
    name="password_change_done",
),
    path(
    "forgot-password/",
    auth_views.PasswordResetView.as_view(
        template_name="users_app/password_reset_form.html",
        email_template_name="users_app/password_reset_email.txt",
        subject_template_name="users_app/password_reset_subject.txt",
    ),
    name="password_reset",
),

path(
    "forgot-password/sent/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="users_app/password_reset_done.html",
    ),
    name="password_reset_done",
),

path(
    "reset-password/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="users_app/password_reset_confirm.html",
    ),
    name="password_reset_confirm",
),

path(
    "reset-password/complete/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="users_app/password_reset_complete.html",
    ),
    name="password_reset_complete",
),
path(
    "emergency-guide/",
    views.emergency_guide,
    name="emergency_guide",
),
path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard",
),

]