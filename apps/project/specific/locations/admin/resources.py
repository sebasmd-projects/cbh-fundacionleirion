from django.db import models
from django.db.models.signals import post_save, pre_delete
from import_export import resources

from ..models import AssetLocationModel, AssetModel
from ..signals import (update_asset_total_quantity_on_location,
                       update_asset_total_quantity_on_location_delete)


class AssetLocationResource(resources.ModelResource):

    def before_import(self, dataset, dry_run, **kwargs):
        print("before_import")
        post_save.disconnect(
            update_asset_total_quantity_on_location, sender=AssetLocationModel)
        pre_delete.disconnect(
            update_asset_total_quantity_on_location_delete, sender=AssetLocationModel)

    def after_import(self, dataset, result, dry_run, **kwargs):
        print("after_import")
        post_save.connect(
            update_asset_total_quantity_on_location, sender=AssetLocationModel
        )
        pre_delete.connect(
            update_asset_total_quantity_on_location_delete, sender=AssetLocationModel
        )

        # Recalcular el total_quantity para cada asset
        for asset in AssetModel.objects.all():
            total_amount = AssetLocationModel.objects.filter(
                asset=asset).aggregate(total=models.Sum('amount'))['total'] or 0
            asset.total_quantity = total_amount
            asset.save()

    class Meta:
        model = AssetLocationModel
