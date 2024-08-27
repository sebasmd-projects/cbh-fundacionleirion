from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import AssetLocationModel, LocationModel


class AssetLocationInline(admin.TabularInline):
    model = AssetLocationModel
    extra = 1
    min_num = 0
    fk_name = 'asset'
    exclude = ('language', 'default_order')


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportActionModelAdmin):
    list_display = ['reference', 'continent', 'owner']
    search_fields = ['reference', 'owner']
    list_filter = ['continent', 'owner']
    ordering = ('default_order','reference','-created')