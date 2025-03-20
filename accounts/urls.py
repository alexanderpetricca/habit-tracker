from django.urls import path, re_path

from accounts import views


urlpatterns = [
    # Authentication
    path("login/", views.CustomLoginView.as_view(), name="account_login"),
    path("logout/", views.CustomLogoutView.as_view(), name="account_logout"),
    path('signup/', views.CustomSignupView.as_view(), name='account_signup'),
    
    # Password Reset
    path("password/reset/", views.CustomPasswordResetView.as_view(), name="account_reset_password"),
    path("password/reset/done/", views.CustomPasswordResetDoneView.as_view(), name="account_reset_password_done"),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.CustomPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    path("password/reset/key/done/", views.CustomPasswordResetFromKeyDoneView.as_view(), name="account_reset_password_from_key_done"),

    # Password Change
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('password/set/', views.PasswordChangeDoneView.as_view(), name='account_change_password_done'),    
    
    # Email Management
    path("email/", views.CustomEmailView.as_view(), name="account_email"),
    path("confirm-email/", views.CustomEmailVerificationSentView.as_view(), name="account_email_verification_sent"),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        views.CustomConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),

    # Other
    path("inactive/", views.CustomAccountInactiveView.as_view(), name="account_inactive"),
]