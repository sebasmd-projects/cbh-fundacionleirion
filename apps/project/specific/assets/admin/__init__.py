
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from ..models import AssetModel
from .actions import update_total_quantities
from .filters import (HasImageFilter, ParentCategoryFilter,
                      ZeroBoxesPerContainerFilter, ZeroTotalQuantityFilter,
                      ZeroUnitsPerBoxFilter)
from .forms import AssetModelForm
from .inlines import AssetLocationInline
from .resources import AssetModelResource


@admin.register(AssetModel)
class AssetModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [AssetLocationInline]

    form = AssetModelForm

    actions = [update_total_quantities]

    def get_export_resource_class(self):
        return AssetModelResource

    search_fields = (
        'id',
        'name',
        'es_name',
        'category__name'
    )

    list_filter = (
        'is_active',
        'quantity_type',
        ZeroTotalQuantityFilter,
        ZeroUnitsPerBoxFilter,
        ZeroBoxesPerContainerFilter,
        ParentCategoryFilter,
        HasImageFilter
    )

    list_display = (
        'es_name',
        'name',
        'category',
        'quantity_type',
        'total_quantity',
        'is_active',
        'units_per_box',
        'boxes_per_container'
    )

    list_display_links = list_display

    readonly_fields = (
        'created',
        'updated',
        'total_quantity',
    )

    ordering = (
        'default_order',
        'created'
    )

    fieldsets = (
        (_('Required Fields'), {'fields': (
            'asset_img',
            'name',
            'es_name',
            'category',
            'quantity_type',
            'total_quantity',
            'is_active',
            'units_per_box',
            'boxes_per_container'
        )}),
        (_('Optional Fields'), {'fields': (
            'observations',
            'asset_year',
            'emission',
            'language',
            'default_order',
        )}),
        (_('Dates'), {'fields': (
            'created',
            'updated'
        )}),
    )
