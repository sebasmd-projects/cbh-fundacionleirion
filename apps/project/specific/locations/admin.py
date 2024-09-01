from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from django.conf import settings

from .models import AssetLocationModel, LocationModel


@admin.register(AssetLocationModel)
class AssetLocationAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = ['location__reference', 'location__owner', 'asset__name', 'asset__es_name']
    autocomplete_fields = ['asset']
    
    def has_module_permission(self, request):
        if request.user.is_superuser or request.user.groups.filter(name=settings.EDIT_ASSETS_LOCATION).exists():
            return True
        return False


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['reference', 'continent', 'owner']
    search_fields = ['reference', 'owner']
    list_filter = ['continent', 'owner']
    ordering = ('default_order', 'reference', 'owner', '-created')
