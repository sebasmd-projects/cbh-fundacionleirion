from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import (EncryptedCharField,
                                      EncryptedDecimalField,
                                      EncryptedPositiveIntegerField,
                                      TimeStampedModel)
from apps.project.specific.bonds.models import BondModel


class SalesModel(TimeStampedModel):
    class SalesTypeChoices(models.TextChoices):
        DIRECT_SALES = "DS", _('Direct Sales')
        RD = 'RD', _('RD')
        OTHER = 'O', _('Other')

    class BuyerTypeChoices(models.TextChoices):
        BANK = 'B', _('Bank')
        ORGANIZATION = 'ON', _('Organization')
        PRIVATE = 'P', _('Private')
        OTHER = 'O', _('Other')

    class CurrencyTypeChoices(models.TextChoices):
        AED = 'AED', _('AED, United Arab Emirates Dirham')
        ARS = 'ARS', _('ARS, Argentine Peso')
        AUD = 'AUD', _('AUD, Australian Dollar')
        BRL = 'BRL', _('BRL, Brazilian Real')
        CAD = 'CAD', _('CAD, Canadian Dollar')
        CHF = 'CHF', _('CHF, Swiss Franc')
        CNY = 'CNY', _('CNY, Chinese Yuan')
        COP = 'COP', _('COP, Colombian Peso')
        DKK = 'DKK', _('DKK, Danish Krone')
        EUR = 'EUR', _('EUR, Euro')
        GBP = 'GBP', _('GBP, British Pound Sterling')
        HKD = 'HKD', _('HKD, Hong Kong Dollar')
        ILS = 'ILS', _('ILS, Israeli New Shekel')
        INR = 'INR', _('INR, Indian Rupee')
        JPY = 'JPY', _('JPY, Japanese Yen')
        KRW = 'KRW', _('KRW, South Korean Won')
        MXN = 'MXN', _('MXN, Mexican Peso')
        MYR = 'MYR', _('MYR, Malaysian Ringgit')
        NOK = 'NOK', _('NOK, Norwegian Krone')
        NZD = 'NZD', _('NZD, New Zealand Dollar')
        PLN = 'PLN', _('PLN, Polish Zloty')
        RUB = 'RUB', _('RUB, Russian Ruble')
        SAR = 'SAR', _('SAR, Saudi Riyal')
        SEK = 'SEK', _('SEK, Swedish Krona')
        SGD = 'SGD', _('SGD, Singapore Dollar')
        THB = 'THB', _('THB, Thai Baht')
        TRY = 'TRY', _('TRY, Turkish Lira')
        TWD = 'TWD', _('TWD, New Taiwan Dollar')
        USD = 'USD', _('USD, United States Dollar')
        ZAR = 'ZAR', _('ZAR, South African Rand')
        ZWD = 'ZWD', _('ZWD, Zimbabwe Dollar')

    bond = models.ForeignKey(
        BondModel,
        on_delete=models.CASCADE,
        related_name="sales_bond",
        verbose_name=_("bond")
    )

    buyer_type = models.CharField(
        _("buyer type"),
        max_length=3,
        choices=BuyerTypeChoices.choices,
        default=BuyerTypeChoices.PRIVATE
    )

    buyer_name = EncryptedCharField(
        _("buyer name"),
        max_length=255
    )

    buyer_country = models.CharField(
        _('country code'),
        max_length=50,
        default='US'
    )

    amount_sold = EncryptedPositiveIntegerField(
        _("amount sold"),
        max_length=255
    )

    sales_type = models.CharField(
        _("sales type"),
        max_length=3,
        choices=SalesTypeChoices.choices,
        default=SalesTypeChoices.DIRECT_SALES
    )

    sale_value = EncryptedDecimalField(
        _("sale value"),
        max_length=255
    )

    sale_currency = models.CharField(
        _("currency"),
        max_length=4,
        choices=CurrencyTypeChoices.choices,
        default=CurrencyTypeChoices.USD
    )

    def __str__(self) -> str:
        return f"{self.bond.name}"

    class Meta:
        db_table = "apps_project_specific_sales_sales"
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")


auditlog.register(
    SalesModel,
    serialize_data=True
)
