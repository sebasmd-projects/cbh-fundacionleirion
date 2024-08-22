from django import forms
from django.contrib import admin
from django_countries import countries
from import_export.admin import ImportExportActionModelAdmin

from .models import SalesModel


class SalesModelAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('buyer_country').initial = 'CO'

    buyer_country = forms.ChoiceField(
        choices=[(code, f'{name} ({code})') for code, name in countries],
        widget=forms.Select(),
        required=False,
    )

    class Meta:
        model = SalesModel
        fields = '__all__'


@admin.register(SalesModel)
class SalesModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    form = SalesModelAdminForm

    search_fields = (
        'bond__name',
    )

    list_filter = (
        'is_active',
        'sales_type',
        'buyer_type'
    )

    list_display = (
        'bond',
        'buyer_type',
        'buyer_country',
        'sales_type',
        'created'
    )

    list_display_links = (
        'bond',
        'buyer_type',
        'buyer_country',
        'sales_type'
    )

    readonly_fields = (
        'created',
        'updated'
    )

    ordering = (
        'default_order',
        'created'
    )
