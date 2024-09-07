from import_export import resources

from ..models import AssetModel


class AssetModelResource(resources.ModelResource):
    def dehydrate_quantity_type(self, asset):
        return asset.get_quantity_type_display()

    def dehydrate_category(self, asset):
        return f"{asset.category.parent} - {asset.category.name}" if asset.category.parent else f"{asset.category.name}"

    class Meta:
        model = AssetModel
