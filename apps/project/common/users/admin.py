from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django_countries import countries
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import UserModel


class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('country_code').initial = 'CO'

        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )

    country_code = forms.ChoiceField(
        choices=[(code, f'{name} ({code})') for code, name in countries],
        widget=forms.Select(),
        required=False,
    )

    password = ReadOnlyPasswordHashField(
        label=_("password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = UserModel
        fields = '__all__'


@admin.register(UserModel)
class UserModelAdmin(UserAdmin, ImportExportActionModelAdmin):
    search_fields = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_display = (
        'get_full_name',
        'username',
        'email',
        'is_staff',
        'is_active'
    )

    list_display_links = (
        'get_full_name',
        'username',
        'email',
    )

    ordering = (
        'default_order',
        'created',
        'last_name',
        'first_name',
        'email',
        'username',
    )

    readonly_fields = (
        'created',
        'updated',
        'last_login'
    )

    fieldsets = (
        (
            _('User Information'), {
                'fields': (
                    'username',
                    'password',
                )
            }
        ),
        (
            _('Personal Information'), {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'country_code'
                )
            }
        ),
        (
            _('Permissions'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                )
            }
        ),
        (
            _('Dates'), {
                'fields': (
                    'last_login',
                    'created',
                    'updated'
                )
            }
        ),
        (
            _('Priority'), {
                'fields': (
                    'default_order',
                )
            }
        )
    )

    form = UserAdminForm

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = _('Names')