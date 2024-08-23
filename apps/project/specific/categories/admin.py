from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import AssetCategoryModel


@admin.register(AssetCategoryModel)
class AssetCategoryModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = ['name', 'parent__name']
    list_filter = ['parent', 'created', 'is_active']
    list_display = ['name', 'parent', 'created']
    list_display_links = ['name']
    ordering = ['default_order', 'name', 'parent', 'created']
    readonly_fields = ['created', 'updated']
