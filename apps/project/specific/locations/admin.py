from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import AssetLocationModel, LocationModel


@admin.register(AssetLocationModel)
class AssetLocationAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = ['location__reference', 'location__owner', 'asset__name', 'asset__es_name']
    autocomplete_fields = ['asset']


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['reference', 'continent', 'owner']
    search_fields = ['reference', 'owner']
    list_filter = ['continent', 'owner']
    ordering = ('default_order', 'reference', 'owner', '-created')
