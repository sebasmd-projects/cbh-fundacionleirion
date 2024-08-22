from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django_countries import countries
from import_export.admin import ImportExportActionModelAdmin

from .models import UserLoginAttemptModel, UserModel


class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('country_code').initial = 'CO'

        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
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
        fields = ['first_name', 'last_name', 'country_code', 'password']  # Campos que puede editar el staff


@admin.register(UserModel)
class UserModelAdmin(UserAdmin, ImportExportActionModelAdmin):
    form = UserAdminForm

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

    readonly_fields = [
        'created',
        'updated',
        'last_login'
    ]

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

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_staff and not request.user.is_superuser:
            self.readonly_fields += [
                'username',
            ]
            
            self.fieldsets = (
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
                            'country_code'
                        )
                    }
                ),
            )
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return queryset.filter(id=request.user.id)
        return queryset

    def has_add_permission(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = _('Names')


admin.site.register(UserLoginAttemptModel)
