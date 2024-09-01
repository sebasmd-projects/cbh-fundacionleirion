from django.db import models

def update_asset_total_quantity_on_location(sender: type[models.Model], instance: models.Model, created: bool, **kwargs) -> None:
    """Updates the total quantity of the associated asset when a new AssetLocation is created."""
    if created:
        asset = instance.asset
        asset.total_quantity += int(instance.amount)
        asset.save()
        print("update_asset_total_quantity_on_location")


def update_asset_total_quantity_on_location_delete(sender: type[models.Model], instance: models.Model, **kwargs) -> None:
    """Updates the total quantity of the associated asset when an AssetLocation is deleted."""
    asset = instance.asset
    asset.total_quantity -= int(instance.amount)
    asset.save()
    print("update_asset_total_quantity_on_location_delete")


def update_asset_total_quantity_on_location_change(sender: type[models.Model], instance: models.Model, **kwargs) -> None:
    """Updates the total quantity of the associated asset when the amount in an AssetLocation changes."""
    if not instance.pk:
        return

    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            difference = int(instance.amount) - int(old_instance.amount)
            asset = instance.asset
            asset.total_quantity += difference
            asset.save()
            print("update_asset_total_quantity_on_location_change")
        except sender.DoesNotExist:
            # TODO Handle the exception as necessary (logging, etc.)
            print("except in update_asset_total_quantity_on_location_change")
            pass


def update_asset_total_quantity_on_location_is_active_change(sender: type[models.Model], instance: models.Model, **kwargs) -> None:
    """Updates the total quantity of the associated asset when the is_active status of an AssetLocation changes."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            asset = instance.asset
            if old_instance.is_active and not instance.is_active:
                asset.total_quantity -= int(instance.amount)
            elif not old_instance.is_active and instance.is_active:
                asset.total_quantity += int(instance.amount)
            asset.save()
            print("update_asset_total_quantity_on_location_is_active_change")
        except sender.DoesNotExist:
            # TODO Handle the exception as necessary (logging, etc.)
            print("except in update_asset_total_quantity_on_location_is_active_change")
            pass
