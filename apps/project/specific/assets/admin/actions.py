
from django.contrib import admin
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


@admin.action(description=_('Update total quantities'))
def update_total_quantities(modeladmin, request, queryset):
    for asset in queryset:
        total_amount = asset.assetlocation_asset.aggregate(
            total=Sum('amount')
        )['total'] or 0
        asset.total_quantity = total_amount
        asset.save()
