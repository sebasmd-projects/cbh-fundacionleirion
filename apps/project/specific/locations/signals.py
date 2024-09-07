import logging

from django.db import DatabaseError, models

logger = logging.getLogger(__name__)


def update_asset_total_quantity_on_location(sender: type[models.Model], instance: models.Model, created: bool, **kwargs) -> None:
    """Updates the total quantity of the associated asset when a new AssetLocation is created."""
    if created:
        try:
            asset = instance.asset
            asset.total_quantity += int(instance.amount)
            asset.save()
        except DatabaseError as e:
            logger.error(
                f"Error updating asset total quantity on location creation: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during location creation: {e}")


def update_asset_total_quantity_on_location_delete(sender: type[models.Model], instance: models.Model, **kwargs) -> None:
    """Updates the total quantity of the associated asset when an AssetLocation is deleted."""
    try:
        asset = instance.asset
        asset.total_quantity -= int(instance.amount)
        asset.save()
    except DatabaseError as e:
        logger.error(f"Error updating asset total quantity on location delete: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error during location deletion: {e}")


def update_asset_total_quantity_on_location_change(sender: type[models.Model], instance: models.Model, **kwargs) -> None:
    """Updates the total quantity of the associated asset when the amount in an AssetLocation changes."""
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        difference = int(instance.amount) - int(old_instance.amount)
        asset = instance.asset
        asset.total_quantity += difference
        asset.save()
    except sender.DoesNotExist:
        logger.warning(f"AssetLocation with pk {instance.pk} does not exist.")
    except DatabaseError as e:
        logger.error(f"Error updating asset total quantity on location change: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error during location change: {e}")


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
        except sender.DoesNotExist:
            logger.warning(f"AssetLocation with pk {instance.pk} does not exist.")
        except DatabaseError as e:
            logger.error(f"Error updating asset total quantity on is_active change: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during is_active change: {e}")
