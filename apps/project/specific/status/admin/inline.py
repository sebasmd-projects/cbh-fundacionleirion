from django.contrib import admin

from ..models import AssetStatusReferenceModel


class AssetStatusReferenceInline(admin.StackedInline):
    model = AssetStatusReferenceModel
    extra = 0
    min_num = 1
    fk_name = 'asset_status'
    verbose_name = "Asset Status Reference"
    exclude = ('language', 'default_order')
    autocomplete_fields = ['supplier']
