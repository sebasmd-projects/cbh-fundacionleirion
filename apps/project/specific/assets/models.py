from auditlog.registry import auditlog
from django.db import models
from django.db.models.signals import (post_delete, post_save, pre_delete,
                                      pre_save)
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel
from apps.project.specific.categories.models import AssetCategoryModel

from .signals import (assets_directory_path, auto_delete_asset_img_on_change,
                      auto_delete_asset_img_on_delete, optimize_image,
                      return_asset_total_quantity_on_delete,
                      validate_and_update_asset_total_quantity)


class AssetModel(TimeStampedModel):
    class QuantityTypeChoices(models.TextChoices):
        UNITS = "U", _("Units")
        CONTAINERS = "C", _("Containers")
        BOXES = "B", _("Boxes")
        OTHER = "O", _("Other")

    asset_img = models.ImageField(
        _("img"),
        upload_to=assets_directory_path,
        blank=True,
        null=True
    )

    name = models.CharField(
        _("english name"),
        max_length=255
    )

    es_name = models.CharField(
        _("spanish name"),
        max_length=255,
    )

    category = models.ForeignKey(
        AssetCategoryModel,
        on_delete=models.CASCADE,
        related_name="asset_assetcategory",
        verbose_name=_("category")
    )

    description = models.TextField(
        _("description"),
        blank=True,
        null=True
    )

    asset_year = models.PositiveIntegerField(
        _("year"),
        blank=True,
        null=True
    )

    emission = models.CharField(
        _("emission"),
        max_length=50,
        blank=True,
        null=True
    )

    quantity_type = models.CharField(
        _("quantity type"),
        max_length=2,
        choices=QuantityTypeChoices.choices,
        default=QuantityTypeChoices.UNITS
    )

    total_quantity = models.PositiveIntegerField(
        _("total lump sum"),
        default=0
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.get_quantity_type_display()}"

    class Meta:
        db_table = "apps_project_specific_assets_asset"
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")
        unique_together = [['name', 'quantity_type']]


class AssetStatusModel(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        AVAILABLE = "A", _("Available")
        RESERVED = "R", _("Reserved")
        SOLD = "S", _("Sold")
        OTHER = "O", _("Other")

    assets = models.ForeignKey(
        AssetModel,
        on_delete=models.CASCADE,
        related_name="assetstatus_asset",
        verbose_name=_("Assets")
    )

    status = models.CharField(
        _("status"),
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.RESERVED
    )

    quantity = models.PositiveIntegerField(
        _("quantity"),
        default=0
    )

    price = models.BigIntegerField(
        _("price"),
        blank=True,
        null=True
    )

    class Meta:
        db_table = "apps_project_specific_assets_status"
        verbose_name = _("Assets Status")
        verbose_name_plural = _("Assets Statuses")

    def __str__(self):
        return f"{self.assets.name} - {self.get_status_display()} - {self.quantity}"


auditlog.register(
    AssetModel,
    serialize_data=True
)

auditlog.register(
    AssetStatusModel,
    serialize_data=True
)

post_save.connect(
    optimize_image,
    sender=AssetModel
)

post_delete.connect(
    auto_delete_asset_img_on_delete,
    sender=AssetModel
)

pre_save.connect(
    auto_delete_asset_img_on_change,
    sender=AssetModel
)

pre_save.connect(
    validate_and_update_asset_total_quantity,
    sender=AssetStatusModel
)

pre_delete.connect(
    return_asset_total_quantity_on_delete,
    sender=AssetStatusModel
)
