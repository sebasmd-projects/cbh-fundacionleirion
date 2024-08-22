from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from .models import BondModel, BondStatusModel

admin.site.register(BondStatusModel, ImportExportActionModelAdmin)


class BondModelForm(forms.ModelForm):
    class Meta:
        model = BondModel
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'rows': 2, 'style': 'width: 80%;'}),
        }


@admin.register(BondModel)
class BondModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    form = BondModelForm

    search_fields = (
        'name',
        'category__name'
    )

    list_filter = (
        'is_active',
        'quantity_type'
    )

    list_display = (
        'name',
        'category',
        'quantity_type',
        'total_quantity',
        'is_active'
    )

    list_display_links = list_display

    readonly_fields = (
        'created',
        'updated'
    )

    ordering = (
        'default_order',
        'created'
    )

    fieldsets = (
        (
            _('Required Fields'),
            {
                'fields': (
                    'name',
                    'category',
                    'quantity_type',
                    'total_quantity',
                    'is_active'
                )
            }
        ),
        (
            _('Optional Fields'),
            {
                'fields': (
                    'bond_year',
                    'emission',
                    'language',
                    'default_order',
                )
            }
        )
    )
