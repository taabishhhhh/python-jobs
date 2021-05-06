from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Email address',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control foo-border',
                'placeholder': 'user@blklab.io'
            }
        )
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control foo-border',
                'placeholder': 'password'
            }
        )
    )

    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password. "
                         "Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        print(args, kwargs, "\n\n context printing")
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not old_password:
            raise forms.ValidationError("Enter valid password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your password doesn't match")
        return old_password

    def clean(self):
        new_pass = self.cleaned_data.get('new_password')
        if not new_pass:
            raise forms.ValidationError(
                {
                    'new_password': 'Please enter a new password'
                }
            )

        confirm_pass = self.cleaned_data.get('confirm_password')
        if not new_pass == confirm_pass:
            raise forms.ValidationError(
                {
                    'confirm_password': 'New passwords do not match each other'
                }
            )

        return self.cleaned_data
