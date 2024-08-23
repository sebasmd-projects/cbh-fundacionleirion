from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import AssetLocationModel, AssetModel, LocationModel


class AssetLocationInline(admin.TabularInline):
    model = AssetLocationModel
    extra = 1
    min_num = 1
    fk_name = 'asset'


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportActionModelAdmin):
    list_display = ['reference', 'continent', 'owner']
    search_fields = ['reference', 'owner']
    list_filter = ['continent', 'owner']
