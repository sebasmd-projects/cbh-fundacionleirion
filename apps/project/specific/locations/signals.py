from django.db import models


def update_asset_total_quantity_on_location(sender: type[models.Model], instance: models.Model, created: bool, **kwargs) -> None:
    """Updates the total quantity of the associated asset when a new AssetLocation is created.

    Args:
        sender (type[models.Model]): The model class that sent the signal.
        instance (models.Model): The instance of the model that was created.
        created (bool): A boolean indicating whether a new record was created.
    """

    if created:
        asset = instance.asset
        asset.total_quantity += instance.amount
        asset.save()


def update_asset_total_quantity_on_location_delete(sender: type[models.Model], instance: models.Model, **kwargs) -> None:
    """Updates the total quantity of the associated asset when an AssetLocation is deleted.

    Args:
        sender (type[models.Model]): The model class that sent the signal.
        instance (models.Model): The instance of the model that was deleted.
    """
    asset = instance.asset
    asset.total_quantity -= instance.amount
    asset.save()


def update_asset_total_quantity_on_location_change(sender: type[models.Model], instance: models.Model, **kwargs) -> None:
    """Updates the total quantity of the associated asset when the amount in an AssetLocation changes.

    Args:
        sender (type[models.Model]): The model class that sent the signal.
        instance (models.Model): The instance of the model that was updated.
    """
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        difference = instance.amount - old_instance.amount
        asset = instance.asset
        asset.total_quantity += difference
        asset.save()


def handle_assetlocation_is_active_change(sender: type[models.Model], instance: models.Model, **kwargs) -> None:
    """Updates the total quantity of the associated asset when the is_active status of an AssetLocation changes.

    Args:
        sender (type[models.Model]): The model class that sent the signal.
        instance (models.Model): The instance of the model that was updated.
    """
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        asset = instance.asset
        if old_instance.is_active and not instance.is_active:
            asset.total_quantity -= instance.amount
        elif not old_instance.is_active and instance.is_active:
            asset.total_quantity += instance.amount
        asset.save()
