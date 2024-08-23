def update_asset_total_quantity_on_location(sender, instance, created, **kwargs):
    if created:
        asset = instance.asset
        asset.total_quantity += instance.amount
        asset.save()