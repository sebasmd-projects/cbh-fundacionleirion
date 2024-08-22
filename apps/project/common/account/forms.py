from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.project.common.users.validators import (
    UnicodeLastNameValidator,
    UnicodeNameValidator,
    UnicodeUsernameValidator
)

UserModel = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label=_('User or Email'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'login_username',
                'type': 'text',
                'placeholder': _('User or Email'),
                'class': 'form-control',
                'aria-label': _('User or Email'),
                'aria-describedby': 'login_username'
            },
        )
    )

    password = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'login_password',
                'type': 'password',
                'placeholder': _('Password'),
                'class': 'form-control',
                'aria-label': _('Password'),
                'aria-describedby': 'login_password'
            }
        )
    )

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username and password:
            if not authenticate(username=username, password=password):
                self.add_error(
                    'password',
                    _('Credentials are invalid')
                )

        return cleaned_data


class UserRegisterForm(forms.ModelForm):
    username_validator = UnicodeUsernameValidator()
    name_validator = UnicodeNameValidator()
    last_name_validator = UnicodeLastNameValidator()

    username = forms.CharField(
        label=_("User"),
        validators=[username_validator],
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "register_username",
                "type": "text",
                "placeholder": _("User"),
                "class": "form-control",
                'aria-label': _('User'),
                'aria-describedby': 'register_username'
            }
        )
    )

    email = forms.CharField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "register_email",
                "type": "email",
                "placeholder": _("Email"),
                "class": "form-control",
                'aria-label': _('Email'),
                'aria-describedby': 'register_email'
            }
        )
    )

    password = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "id": "register_password",
                'type': 'password',
                'placeholder': _('Password'),
                'class': 'form-control',
                'aria-label': _('Password'),
                'aria-describedby': 'register_password'
            }
        )
    )

    confirm_password = forms.CharField(
        label=_('Confirm Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "id": "register_confirm_password",
                "type": "password",
                "placeholder": _('Confirm Password'),
                "class": "form-control",
                'aria-label': _('Confirm Password'),
                'aria-describedby': 'register_confirm_password'
            }
        )
    )

    first_name = forms.CharField(
        label=_("Names"),
        required=True,
        validators=[name_validator],
        widget=forms.TextInput(
            attrs={
                "id": "register_first_name",
                "type": "text",
                "placeholder": _("Nombres"),
                "class": "form-control",
                'aria-label': _('Nombres'),
                'aria-describedby': 'register_first_name'
            }
        )
    )

    last_name = forms.CharField(
        label=_("Last names"),
        required=True,
        validators=[last_name_validator],
        widget=forms.TextInput(
            attrs={
                "id": "register_last_name",
                "type": "text",
                "placeholder": _("Last names"),
                "class": "form-control",
                'aria-label': _('Last names'),
                'aria-describedby': 'register_last_name'
            }
        )
    )

    def clean_confirm_password(self):
        validate_password(
            self.cleaned_data["password"],
        )

        validate_password(
            self.cleaned_data["confirm_password"],
        )

        if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            raise ValidationError(_('Passwords do not match'))

    class Meta:
        model = UserModel
        fields = (
            "username",
            "email",
            "first_name",
            "last_name"
        )


class UserUpdateProfile(forms.ModelForm):
    pass