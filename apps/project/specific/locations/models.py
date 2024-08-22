from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel
from apps.project.specific.bonds.models import BondModel


class LocationModel(TimeStampedModel):
    name = models.CharField(
        _("name"),
        max_length=150
    )

    description = models.TextField(
        _("description"),
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "apps_project_specific_locations_location"
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")


class BondLocationModel(TimeStampedModel):
    bond = models.ForeignKey(
        BondModel,
        on_delete=models.CASCADE,
        related_name="bondlocation_bond",
        verbose_name=_("bond")
    )

    location = models.ForeignKey(
        LocationModel,
        on_delete=models.CASCADE,
        related_name="bondlocation_location",
        verbose_name=_("location"),
    )

    def __str__(self) -> str:
        return f"{self.bond.name} - {self.location.name}"

    class Meta:
        db_table = "apps_project_specific_locations_bondlocation"
        verbose_name = _("Bond Location")
        verbose_name_plural = _("Bond Locations")


auditlog.register(
    LocationModel,
    serialize_data=True
)

auditlog.register(
    BondLocationModel,
    serialize_data=True
)
