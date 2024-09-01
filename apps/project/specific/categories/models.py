from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel


class AssetCategoryModel(TimeStampedModel):
    name = models.CharField(
        _("category"),
        max_length=50,
    )

    description = models.TextField(
        _("description"),
        blank=True,
        null=True
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="assetcategory_assetcategory",
        verbose_name=_("parent category"),
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        message = f"{self.name}"

        if self.parent:
            message = f"{self.parent} - {self.name}"

        return f"{message}"

    class Meta:
        db_table = "apps_project_specific_categories_assetcategory"
        verbose_name = _('Asset Category')
        verbose_name_plural = _('Assets Categories')
        ordering = ["default_order", "name", "-created"]

auditlog.register(
    AssetCategoryModel,
    serialize_data=True
)
