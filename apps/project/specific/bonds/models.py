from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel
from apps.project.specific.categories.models import BondCategoryModel


class BondModel(TimeStampedModel):
    class QuantityTypeChoices(models.TextChoices):
        UNITS = "U", _("Units")
        CONTAINERS = "C", _("Containers")
        BOXES = "B", _("Boxes")
        OTHER = "O", _("Other")

    name = models.CharField(
        _("name"),
        max_length=150
    )

    category = models.ForeignKey(
        BondCategoryModel,
        on_delete=models.CASCADE,
        related_name="bond_bondcategory",
        verbose_name=_("category")
    )

    description = models.TextField(
        _("description"),
        blank=True,
        null=True
    )

    bond_year = models.PositiveIntegerField(
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
        return self.name

    class Meta:
        db_table = "apps_project_specific_bonds_bond"
        verbose_name = _("Bond")
        verbose_name_plural = _("Bonds")


class BondStatusModel(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        AVAILABLE = "A", _("Available")
        RESERVED = "R", _("Reserved")
        SOLD = "S", _("Sold")
        OTHER = "O", _("Other")

    bond = models.ForeignKey(
        BondModel,
        on_delete=models.CASCADE,
        related_name="bondstatus_bond",
        verbose_name=_("bond")
    )

    status = models.CharField(
        _("status"),
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE
    )

    quantity = models.PositiveIntegerField(
        _("quantity"),
        default=0
    )

    class Meta:
        db_table = "apps_project_specific_bonds_status"
        verbose_name = _("Bond Status")
        verbose_name_plural = _("Bond Statuses")

    def __str__(self):
        return f"{self.bond.name} - {self.get_status_display()} - {self.quantity}"


auditlog.register(
    BondModel,
    serialize_data=True
)

auditlog.register(
    BondStatusModel,
    serialize_data=True
)
