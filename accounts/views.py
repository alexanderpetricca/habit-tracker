from django.views.generic import TemplateView
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.account.views import (
    LoginView, 
    LogoutView, 
    SignupView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,    
    PasswordChangeView,
    EmailView,
    ConfirmEmailView,
    EmailVerificationSentView,
    AccountInactiveView, 
)


class CustomLoginView(LoginView):
    """
    Allauth override for LoginView.
    """    
    
    pass


class CustomLogoutView(LogoutView):
    """
    Allauth override for LogoutView.
    """
    
    pass


class CustomSignupView(SignupView):
    """
    Allauth override for SignupView.
    """

    pass
    

class CustomPasswordResetView(PasswordResetView):
    """
    Allauth override for PasswordResetView.
    """

    pass


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Allauth override for PasswordResetDoneView.
    """    
    
    pass


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    """
    Allauth override for PasswordResetFromKeyView.
    """

    pass


class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    """
    Allauth override for PasswordResetFromKeyDoneView.
    """

    pass


class CustomPasswordChangeView(PasswordChangeView):
    """
    Allauth override for PasswordChangeView.
    """

    def get_success_url(self):
        success_url = reverse('account_change_password_done')
        return success_url


class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    """
    Renders confirmation page when user changes password.
    """
    
    template_name = 'account/password_change_done.html'


class CustomEmailView(EmailView):
    """
    Allauth override for EmailView.
    """

    pass


class CustomEmailVerificationSentView(EmailVerificationSentView):
    """
    Allauth override for EmailVerificationSentView.
    """
    
    pass


class CustomConfirmEmailView(ConfirmEmailView):
    """
    Allauth override for ConfirmEmailView.
    """
    
    pass


class CustomAccountInactiveView(AccountInactiveView):
    """
    Allauth override for AccountInactiveView.
    """
    
    pass