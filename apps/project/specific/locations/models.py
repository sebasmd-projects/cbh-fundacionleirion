from auditlog.registry import auditlog
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel
from apps.project.specific.assets.models import AssetModel

from .signals import update_asset_total_quantity_on_location


class LocationModel(TimeStampedModel):
    class ContinentChoices(models.TextChoices):
        ASIA = "AS", _("Asia")
        NORTH_AMERICA = "NA", _("North America")
        CENTRAL_AMERICA = "CA", _("Central America")
        SOUTH_AMERICA = "SA", _("South America")
        AFRICA = "AF", _("Africa")
        ANTARCTICA = "AN", _("Antarctica")
        EUROPE = "EU", _("Europe")
        OCEANIA = "OC", _("Oceania")

    reference = models.CharField(
        _("reference"),
        max_length=150
    )

    description = models.TextField(
        _("description"),
        blank=True,
        null=True
    )

    continent = models.CharField(
        _("continent"),
        max_length=3,
        choices=ContinentChoices.choices,
        default=ContinentChoices.EUROPE
    )

    owner = models.CharField(
        _("owner"),
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        message = f"{self.reference} - {self.get_continent_display()}"
        if self.owner:
            message = f"{self.reference} - {self.get_continent_display()} - {self.owner}"
        return message

    class Meta:
        db_table = "apps_project_specific_locations_location"
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")


class AssetLocationModel(TimeStampedModel):
    asset = models.ForeignKey(
        AssetModel,
        on_delete=models.CASCADE,
        related_name="assetlocation_asset",
        verbose_name=_("Assets")
    )

    location = models.ForeignKey(
        LocationModel,
        on_delete=models.CASCADE,
        related_name="assetlocation_location",
        verbose_name=_("location"),
    )

    amount = models.BigIntegerField(
        _("amount")
    )

    def __str__(self) -> str:
        return f"{self.asset.name} - {self.location.reference} - {self.amount}"

    class Meta:
        db_table = "apps_project_specific_locations_assetlocation"
        verbose_name = _("Assets Location")
        verbose_name_plural = _("Assets Locations")


auditlog.register(
    LocationModel,
    serialize_data=True
)

auditlog.register(
    AssetLocationModel,
    serialize_data=True
)

post_save.connect(
    update_asset_total_quantity_on_location,
    sender=AssetLocationModel
)
