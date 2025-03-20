from django.contrib.auth import forms as auth_forms
from django import forms

from allauth.account.forms import (
    LoginForm,
    SignupForm,
    ChangePasswordForm, 
    ResetPasswordForm, 
    ResetPasswordKeyForm,
)

from .models import CustomUser



# Admin ----

class CustomUserAdminCreateForm(auth_forms.UserCreationForm):
    """
    Form used to create a user in the admin backend.
    """

    class Meta:
        model = CustomUser
        fields = ('__all__')


class CustomUserAdminChangeForm(auth_forms.UserChangeForm):
    """
    Form used to update a user in the admin backend.
    """

    class Meta:
        model = CustomUser
        fields = ('__all__')


# Allauth ----

class CustomSignupForm(SignupForm):
    """
    Override settings on AllAuth signup form.
    """

    organisation_name = forms.CharField(
        required=True, 
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Company Name',
            }
        )
    )
    

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].label = ""
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email Address',
        })
        
        self.fields['password1'].label = ""
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
        })

        self.fields['password2'].label = ""
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
        })        


class CustomLoginForm(LoginForm):
    """
    Override settings on AllAuth login form.
    """

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        
        self.fields['login'].label = ""
        self.fields['login'].widget.attrs.update({
            'placeholder': 'Email Address',
        })
        
        self.fields['password'].label = ""
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
        })


class CustomPasswordResetForm(ResetPasswordForm):
    """
    Override settings on AllAuth reset password form.
    """    
    
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = ""        
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email Address',
        })


    def save(self, *args, **kwargs):
        # Check if user exists (blank list if not, so email not sent)
        if self.users:
            super().save(*args, **kwargs)        


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    """
    Override settings on AllAuth reset password from key form.
    """    
    
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)

        self.fields['password1'].label = ""
        self.fields['password1'].help_text = ""
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'New Password',
        })
        
        self.fields['password2'].label = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm New Password',
        })         


class CustomPasswordChangeForm(ChangePasswordForm):
    """
    Override settings on AllAuth change password form.
    """
    
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['oldpassword'].label = ""
        self.fields['oldpassword'].widget.attrs.update({
            'placeholder': 'Current Password',
        })
        
        self.fields['password1'].label = ""
        self.fields['password1'].help_text = ""
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'New Password',
        })
        
        self.fields['password2'].label = ""
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm New Password',
        })