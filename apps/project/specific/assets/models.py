from auditlog.registry import auditlog
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel
from apps.project.specific.categories.models import AssetCategoryModel

from .signals import (assets_directory_path, auto_delete_asset_img_on_change,
                      auto_delete_asset_img_on_delete, optimize_image)


class AssetModel(TimeStampedModel):
    class QuantityTypeChoices(models.TextChoices):
        UNITS = "U", _("Units")
        CONTAINERS = "C", _("Containers")
        BOXES = "B", _("Boxes")
        OTHER = "O", _("Other")

    asset_img = models.ImageField(
        _("img"),
        max_length=255,
        upload_to=assets_directory_path,
        blank=True,
        null=True
    )

    observations = models.TextField(
        _("observations"),
        default="",
        blank=True,
        null=True
    )

    units_per_box = models.BigIntegerField(
        _("units per box"),
        default=0
    )

    boxes_per_container = models.BigIntegerField(
        _("boxes per container"),
        default=0
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

    total_quantity = models.BigIntegerField(
        _("total lump sum"),
        default=0
    )

    def asset_total_quantity(self):
        # total quantity matches the sum of all related asset locations.
        expected_total = self.assetlocation_asset.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        return expected_total
        if self.total_quantity != expected_total:
            self.total_quantity = expected_total

    def __str__(self) -> str:
        return f"{self.es_name} - {self.get_quantity_type_display()} - {self.total_quantity}"

    class Meta:
        db_table = "apps_project_specific_assets_asset"
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")
        unique_together = [['name', 'quantity_type']]
        ordering = ["default_order", "es_name", "-created"]


# Connect signals to the model
post_save.connect(optimize_image, sender=AssetModel)
post_delete.connect(auto_delete_asset_img_on_delete, sender=AssetModel)
pre_save.connect(auto_delete_asset_img_on_change, sender=AssetModel)

# Register the model with audit log for tracking changes
auditlog.register(AssetModel, serialize_data=True)
