from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from apps.project.specific.locations.admin import AssetLocationInline

from .models import AssetModel, AssetStatusModel

admin.site.register(AssetStatusModel, ImportExportActionModelAdmin)


class AssetModelForm(forms.ModelForm):
    class Meta:
        model = AssetModel
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'rows': 2, 'style': 'width: 80%;'}),
            'es_name': forms.Textarea(attrs={'rows': 2, 'style': 'width: 80%;'}),
        }


@admin.register(AssetModel)
class AssetModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [AssetLocationInline]

    form = AssetModelForm

    search_fields = (
        'name',
        'es_name',
        'category__name'
    )

    list_filter = (
        'is_active',
        'quantity_type'
    )

    list_display = (
        'es_name',
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
                    'asset_img',
                    'name',
                    'es_name',
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
                    'asset_year',
                    'emission',
                    'language',
                    'default_order',
                )
            }
        )
    )
