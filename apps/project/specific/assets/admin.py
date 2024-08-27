from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from apps.project.specific.categories.models import AssetCategoryModel
from apps.project.specific.locations.admin import AssetLocationInline

from .models import AssetModel, AssetStatusModel

admin.site.register(AssetStatusModel, ImportExportActionModelAdmin)


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


class ParentCategoryFilter(SimpleListFilter):
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


class AssetModelForm(forms.ModelForm):
    class Meta:
        model = AssetModel
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'rows': 2, 'style': 'width: 80%;'}),
            'es_name': forms.Textarea(attrs={'rows': 2, 'style': 'width: 80%;'}),
        }


@admin.register(AssetModel)
class AssetModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [AssetLocationInline]

    form = AssetModelForm

    search_fields = (
        'name',
        'es_name',
        'category__name'
    )

    list_filter = (
        'is_active',
        'quantity_type',
        ZeroTotalQuantityFilter,
        ZeroUnitsPerBoxFilter,
        ZeroBoxesPerContainerFilter,
        ParentCategoryFilter
    )

    list_display = (
        'es_name',
        'name',
        'category',
        'quantity_type',
        'total_quantity',
        'is_active',
        'units_per_box',
        'boxes_per_container'
    )

    list_display_links = list_display

    readonly_fields = (
        'created',
        'updated'
    )

    ordering = (
        'default_order',
        'created'
    )

    fieldsets = (
        (
            _('Required Fields'),
            {
                'fields': (
                    'asset_img',
                    'name',
                    'es_name',
                    'category',
                    'quantity_type',
                    'total_quantity',
                    'is_active',
                    'units_per_box',
                    'boxes_per_container'
                )
            }
        ),
        (
            _('Optional Fields'),
            {
                'fields': (
                    'asset_year',
                    'emission',
                    'language',
                    'default_order',
                    'observations'
                )
            }
        )
    )
