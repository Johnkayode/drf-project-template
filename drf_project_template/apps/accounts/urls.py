from allauth.account import views as allauth_views
from django.contrib.auth import views as django_auth_views
from django.urls import path, re_path
from django.views.generic import TemplateView
from dj_rest_auth import views as dj_rest_auth_views
from dj_rest_auth.registration import views as dj_rest_auth_registration_views
from drf_project_template.apps.accounts import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify-email"),
    path(
        "resend-verification-email/",
        dj_rest_auth_registration_views.ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),

    # allauth
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        TemplateView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "account-email-verification-sent/",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "password/reset/",
        dj_rest_auth_views.PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "password/reset/confirm/",
        dj_rest_auth_views.PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path(
        "password/change/",
        dj_rest_auth_views.PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path(
        "reset/<uidb64>/<token>/",
        django_auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        allauth_views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "user/", dj_rest_auth_views.UserDetailsView.as_view(), name="rest_user_details"
    ),
]