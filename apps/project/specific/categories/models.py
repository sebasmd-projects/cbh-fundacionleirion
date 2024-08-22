from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel


class BondCategoryModel(TimeStampedModel):
    name = models.CharField(
        _("name"),
        max_length=50
    )

    description = models.TextField(
        _("description"),
        blank=True,
        null=True
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="bondcategory_bondcategory",
        verbose_name=_("sub category"),
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "apps_project_specific_categories_bondcategory"
        verbose_name = _('Bond Category')
        verbose_name_plural = _('Bond Categories')


auditlog.register(
    BondCategoryModel,
    serialize_data=True
)
