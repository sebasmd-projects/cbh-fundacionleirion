import logging
from decimal import Decimal

from auditlog.models import AuditlogHistoryField
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class EncryptedField(models.CharField):
    """Custom field for storing encrypted data in the database.

    Args:
        models.CharField (class): Base Django CharField class.
    """

    def __init__(self, *args, **kwargs):
        self.cipher = Fernet(settings.ENCODED_KEY)
        self.data_type = kwargs.pop('data_type', str)
        super().__init__(*args, **kwargs)

    def encrypt(self, value: any) -> str:
        """Encrypts the given value.

        Args:
            value (any): The value to encrypt.

        Returns:
            str: The encrypted value as a string.
        """
        if value is None:
            return value
        value_str = str(value)
        encrypted_value = self.cipher.encrypt(value_str.encode('utf-8'))
        return encrypted_value.decode('utf-8')

    def decrypt(self, value: any) -> any:
        """Decrypts the given value.

        Args:
            value (str): The encrypted value to decrypt.

        Raises:
            ValidationError: If the decryption fails.

        Returns:
            any: The decrypted value, converted to the appropriate data type.
        """
        if value is None or value.startswith("****"):
            return value
        try:
            decrypted_value = self.cipher.decrypt(
                value.encode('utf-8')
            ).decode('utf-8')
        except Exception:
            raise ValidationError("Error decrypting the value")

        type_map = {
            int: int,
            Decimal: Decimal,
            bool: lambda x: x.lower() == 'true'
        }

        return type_map.get(self.data_type, str)(decrypted_value)

    def get_prep_value(self, value: any) -> str:
        """Prepares the value for saving to the database by encrypting it.

        Args:
            value (any): The value to prepare.

        Returns:
            str: The encrypted value.
        """
        if isinstance(value, str) and value.startswith('gAAAAA'):
            return value
        return self.encrypt(value)

    def from_db_value(self, value: str, expression: any, connection: any) -> any:
        """Converts the encrypted value from the database back to its original form.

        Args:
            value (str): The encrypted value from the database.
            expression (any): The expression used in the query.
            connection (any): The database connection used for the query.

        Returns:
            any: The decrypted value if the user has access; otherwise, a masked value.
        """
        return self.decrypt(value)

    def to_python(self, value: any) -> any:
        """Converts the value to the appropriate Python data type.

        Args:
            value (any): The value to convert.

        Returns:
            any: The value converted to its appropriate data type.
        """
        if value is None:
            return None

        if isinstance(value, self.data_type):
            return value

        try:
            # Attempt to convert the value to the expected data type
            return self.data_type(value)
        except (ValueError, TypeError) as e:
            # Log an error or raise an exception if the conversion fails
            logger.error(
                _(f"Cannot convert value {value} to {self.data_type}: {e}")
            )
            raise


class EncryptedCharField(EncryptedField):
    """Custom field for storing encrypted string data.

    Args:
        EncryptedField (class): Base class for encrypted fields.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super().__init__(data_type=str, *args, **kwargs)


class EncryptedDecimalField(EncryptedField):
    """Custom field for storing encrypted decimal data.

    Args:
        EncryptedField (class): Base class for encrypted fields.
        models.CharField (class): Django model field for character data.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super().__init__(data_type=Decimal, *args, **kwargs)


class EncryptedIntegerField(EncryptedField):
    """Custom field for storing encrypted integer data.

    Args:
        EncryptedField (class): Base class for encrypted fields.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super().__init__(data_type=int, *args, **kwargs)


class EncryptedBooleanField(EncryptedField):
    """Custom field for storing encrypted boolean data.

    Args:
        EncryptedField (class): Base class for encrypted fields.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super().__init__(data_type=bool, *args, **kwargs)


class TimeStampedModel(models.Model):
    """Abstract model providing timestamp fields (created and updated) and additional metadata.

    Args:
        models.Model (class): Base Django model class.
    """
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
        abstract = True
        ordering = ['default_order']
