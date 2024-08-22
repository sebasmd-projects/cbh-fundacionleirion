import base64
import decimal

from auditlog.models import AuditlogHistoryField
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

utils_path: str = settings.UTILS_PATH
utils_db_name = utils_path.replace('.', '_')


class TimeStampedModel(models.Model):
    """A base model class with timestamp fields."""
    history = AuditlogHistoryField()

    language_choices = [
        ('es', _('Spanish')),
        ('en', _('English')),
    ]

    language = models.CharField(
        _("language"),
        max_length=4,
        choices=language_choices,
        default='es',
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        _('created'),
        default=timezone.now,
        editable=False
    )

    updated = models.DateTimeField(
        _('updated'),
        auto_now=True,
        editable=False
    )

    is_active = models.BooleanField(
        _("is active"),
        default=True
    )

    default_order = models.PositiveIntegerField(
        _('priority'),
        default=1,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
        ordering = ['default_order']


class EncryptedField(models.Field):
    def __init__(self, *args, **kwargs):
        self.cipher = Fernet(settings.ENCODED_KEY)
        self.data_type = kwargs.pop('data_type', str)
        super().__init__(*args, **kwargs)

    def encrypt(self, value):
        if value is None:
            return value
        value_str = str(value)
        encrypted_value = self.cipher.encrypt(value_str.encode('utf-8'))
        return encrypted_value.decode('utf-8')

    def decrypt(self, value: str | None):
        if value is None:
            return value

        decrypted_value = self.cipher.decrypt(
            value.encode('utf-8')).decode('utf-8')

        if self.data_type == int:
            return int(decrypted_value)

        elif self.data_type == decimal.Decimal:
            return decimal.Decimal(decrypted_value)

        elif self.data_type == bool:
            return decrypted_value.lower() == 'true'

        return decrypted_value

    def get_prep_value(self, value):
        return self.encrypt(value)

    def from_db_value(self, value, expression, connection):
        return self.decrypt(value)

    def to_python(self, value):
        if isinstance(value, self.data_type) or value is None:
            return value

        return self.decrypt(value)


class EncryptedCharField(EncryptedField, models.CharField):
    data_type = str


class EncryptedDecimalField(EncryptedField, models.CharField):
    data_type = decimal.Decimal


class EncryptedIntegerField(EncryptedField, models.CharField):
    data_type = int


class EncryptedPositiveIntegerField(EncryptedField, models.CharField):
    data_type = int


class EncryptedBooleanField(EncryptedField, models.CharField):
    data_type = bool
