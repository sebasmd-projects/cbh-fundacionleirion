from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.project.specific.categories.models import AssetCategoryModel


class ZeroTotalQuantityFilter(admin.SimpleListFilter):
    title = _('Total Quantity Zero')
    parameter_name = 'total_quantity_zero'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(total_quantity=0)
        if self.value() == 'no':
            return queryset.exclude(total_quantity=0)
        return queryset


class ZeroUnitsPerBoxFilter(admin.SimpleListFilter):
    title = _('Units per Box Zero')
    parameter_name = 'units_per_box_zero'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(units_per_box=0)
        if self.value() == 'no':
            return queryset.exclude(units_per_box=0)
        return queryset


class ZeroBoxesPerContainerFilter(admin.SimpleListFilter):
    title = _('Boxes per Container Zero')
    parameter_name = 'boxes_per_container_zero'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(boxes_per_container=0)
        if self.value() == 'no':
            return queryset.exclude(boxes_per_container=0)
        return queryset


class ParentCategoryFilter(admin.SimpleListFilter):
    title = _('Parent Category')
    parameter_name = 'parent_category'

    def lookups(self, request, model_admin):
        # Mostrar solo categorías padre en el filtro
        parent_categories = AssetCategoryModel.objects.filter(
            parent__isnull=True)
        return [(cat.id, cat.name) for cat in parent_categories]

    def queryset(self, request, queryset):
        if self.value():
            # Obtener la categoría padre seleccionada
            parent_category = AssetCategoryModel.objects.get(pk=self.value())
            # Filtrar por la categoría padre o sus hijas
            return queryset.filter(category__in=[parent_category] + list(parent_category.assetcategory_assetcategory.all()))
        return queryset


class HasImageFilter(admin.SimpleListFilter):
    title = _('Has Image')
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(asset_img__isnull=True).exclude(asset_img__exact='')
        if self.value() == 'no':
            return queryset.filter(models.Q(asset_img__isnull=True) | models.Q(asset_img__exact=''))
        return queryset
