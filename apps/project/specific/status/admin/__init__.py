
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from ..models import AssetStatusModel, AssetStatusReferenceModel
from .inline import AssetStatusReferenceInline


@admin.register(AssetStatusReferenceModel)
class AssetStatusReferenceAdmin(admin.ModelAdmin):
    search_fields = (
        'asset_status__buyer',
        'asset_status__price'
    )

    list_display = (
        'get_asset_status_buyer',
        'get_asset_status_price',
        'get_supplier_asset_es_name',
        'get_supplier_location',
        'get_status_display',
        'amount'
    )

    list_display_links = list_display[:3]

    ordering = (
        'default_order',
        'created'
    )

    fieldsets = (
        (_('Required Fields'), {"fields": ('asset_status',
         'supplier', 'status', 'amount', 'is_active'), }),
        (_('Dates'), {'fields': ('created', 'updated')}),
        (_('Other fields'), {'fields': ('language', 'default_order')}),
    )
    
    readonly_fields = (
        'created',
        'updated',
    )

    def has_module_permission(self, request):
        if request.user.is_superuser or request.user.groups.filter(name=settings.EDIT_ASSETS_STATUS_REFERENCE).exists():
            return True
        return False

    def get_asset_status_buyer(self, obj):
        return obj.asset_status.buyer

    def get_asset_status_price(self, obj):
        return obj.asset_status.price

    def get_supplier_asset_es_name(self, obj):
        return obj.supplier.asset.es_name

    def get_supplier_location(self, obj):
        return f"{obj.supplier.location.reference} | {obj.supplier.location.owner} | {obj.supplier.location.get_continent_display()}"

    def get_status_display(self, obj):
        return obj.get_status_display()

    get_asset_status_buyer.short_description = _("buyer")

    get_asset_status_price.short_description = _("price")

    get_supplier_asset_es_name.short_description = _("asset")

    get_supplier_location.short_description = _("location")

    get_status_display.short_description = _("status")


@admin.register(AssetStatusModel)
class AssetStatusAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [AssetStatusReferenceInline]

    list_display = (
        'buyer', 'price',
        'asset_name', 'observations',
        'description', 'total_amount',
        
    )

    list_display_links = list_display[:3]

    search_fields = (
        'buyer', 'description',
        'price', 'observations'
    )

    fieldsets = (
        (_('Required Fields'), {'fields': ('buyer', 'price', 'total_amount')}),
        (_('Dates'), {'fields': ('created', 'updated')}),
        (_('Other fields'), {'fields': ('observations',
         'description', 'language', 'default_order')}),
    )

    readonly_fields = ('created', 'updated', 'total_amount')

    ordering = (
        'default_order',
        'created'
    )

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
