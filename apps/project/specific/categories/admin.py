from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from .models import AssetCategoryModel


class ParentCategoryFilter(SimpleListFilter):
    title = _('Parent Category')
    parameter_name = 'parent_category'

    def lookups(self, request, model_admin):
        parent_categories = AssetCategoryModel.objects.filter(
            parent__isnull=True)
        return [(cat.id, cat.name) for cat in parent_categories]

    def queryset(self, request, queryset):
        if self.value():
            # Obtener la categoría padre seleccionada
            parent_category = AssetCategoryModel.objects.get(pk=self.value())
            # Filtrar por la categoría padre o sus hijas
            return queryset.filter(models.Q(id=parent_category.id) | models.Q(parent=parent_category))
        return queryset


@admin.register(AssetCategoryModel)
class AssetCategoryModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = ['name', 'parent__name']
    list_filter = ['created', 'is_active', ParentCategoryFilter]
    list_display = ['name', 'parent', 'created']
    list_display_links = ['name']
    ordering = ['default_order', 'name', 'parent', 'created']
    readonly_fields = ['created', 'updated']
