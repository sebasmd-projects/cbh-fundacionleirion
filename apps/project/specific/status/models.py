from typing import Iterable

from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel
from apps.project.specific.locations.models import AssetLocationModel


class AssetStatusModel(TimeStampedModel):

    price = models.DecimalField(
        _("price"),
        decimal_places=4,
        max_digits=60,
        blank=True,
        null=True
    )

    buyer = models.CharField(
        _("buyer"),
        max_length=255,
        blank=True,
        null=True
    )

    observations = models.TextField(
        _("observations"),
        blank=True,
        null=True
    )

    description = models.TextField(
        _("description"),
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.buyer} - {self.price}"

    class Meta:
        db_table = "apps_project_specific_status_status"
        verbose_name = _("Assets Status")
        verbose_name_plural = _("Assets Statuses")
        ordering = ["default_order", "-created", "buyer"]


class AssetStatusReferenceModel(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        AVAILABLE = "A", _("Available")
        RESERVED = "R", _("Reserved")
        SOLD = "S", _("Sold")
        OTHER = "O", _("Other")

    asset_status = models.ForeignKey(
        AssetStatusModel,
        on_delete=models.CASCADE,
        related_name="assetstatus_references",
        verbose_name=_("asset status")
    )

    supplier = models.ForeignKey(
        AssetLocationModel,
        on_delete=models.CASCADE,
        related_name="assetstatusreference_location",
        verbose_name=_("supplier")
    )

    status = models.CharField(
        _("status"),
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.RESERVED
    )

    amount = models.BigIntegerField(
        _("amount")
    )

    def __str__(self):
        return f"{self.get_status_display()} - {self.amount}"

    class Meta:
        db_table = "apps_project_specific_status_statusreference"
        verbose_name = _("Assets Status Reference")
        verbose_name_plural = _("Assets Statuses References")


auditlog.register(
    AssetStatusModel,
    serialize_data=True
)

auditlog.register(
    AssetStatusReferenceModel,
    serialize_data=True
)
