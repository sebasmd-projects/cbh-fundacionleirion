
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from ..models import AssetStatusModel, AssetStatusReferenceModel
from .inline import AssetStatusReferenceInline

admin.site.register(AssetStatusReferenceModel)

@admin.register(AssetStatusModel)
class AssetStatusAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [AssetStatusReferenceInline]

    list_display = ('buyer', 'price', 'asset_name', 'observations',
                    'description', 'total_amount', )

    search_fields = ('buyer', 'description', 'price', 'observations')
    
    fieldsets = (
        (None, {
            'fields': ('buyer', 'price', 'observations', 'description', 'total_amount')
        }),
    )
    
    readonly_fields = ('created', 'updated', 'total_amount')

    def total_amount(self, obj):
        total = AssetStatusReferenceModel.objects.filter(
            asset_status=obj
        ).aggregate(
            total=models.Sum('amount')
        )['total']

        return total or 0

    total_amount.short_description = _("Total Amount")

    def asset_name(self, obj):
        # Obtener el primer AssetStatusReferenceModel relacionado
        asset_status_reference = AssetStatusReferenceModel.objects.filter(
            asset_status=obj
        ).first()
        if asset_status_reference:
            # Obtener el AssetModel a través de la relación supplier
            asset = asset_status_reference.supplier.asset
            if asset:
                return asset.es_name
        return 'N/A'

    asset_name.short_description = _("Asset Name")
