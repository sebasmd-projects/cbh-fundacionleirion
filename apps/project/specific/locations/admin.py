from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from .models import AssetLocationModel, LocationModel


@admin.register(AssetLocationModel)
class AssetLocationAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = (
        'location__reference', 'location__owner',
        'asset__name', 'asset__es_name'
    )

    autocomplete_fields = ('asset',)

    list_display = (
        'get_location_owner',
        'get_location_reference',
        'get_location_continent',
        'amount',
        'get_asset_es_name',
    )
    
    list_display_links = list_display[:3]

    readonly_fields = (
        'created',
        'updated',
    )
    
    ordering = (
        'default_order',
        'created'
    )

    fieldsets = (
        (_('Required Fields'), {"fields": ('asset', 'location', 'amount', 'is_active'),}),
        (_('Dates'), {'fields': ('created','updated')}),
        (_('Other fields'), {'fields': ('language', 'default_order')}),
    )
    
    
    def has_module_permission(self, request):
        if request.user.is_superuser or request.user.groups.filter(name=settings.EDIT_ASSETS_LOCATION).exists():
            return True
        return False

    def get_asset_es_name(self, obj):
        return obj.asset.es_name

    def get_location_reference(self, obj):
        return obj.location.reference

    def get_location_continent(self, obj):
        return obj.location.get_continent_display()

    def get_location_owner(self, obj):
        return obj.location.owner

    get_asset_es_name.short_description = _("spanish name")

    get_location_reference.short_description = _("reference")

    get_location_continent.short_description = _("continent")

    get_location_owner.short_description = _("owner")


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('reference', 'continent', 'owner')
    search_fields = ('reference', 'owner')
    list_filter = ('continent', 'owner')
    ordering = ('default_order', 'reference', 'owner', '-created')
    readonly_fields = ('created', 'updated',)
    fieldsets = (
        (_('Required Fields'), {'fields': ('reference', 'continent',)}),
        (_('Optional Fields'), {'fields': ('owner', 'description',)}),
        (_('Dates'), {'fields': ('created', 'updated')}),
        (_('Other fields'), {'fields': ('language', 'default_order')}),
    )
