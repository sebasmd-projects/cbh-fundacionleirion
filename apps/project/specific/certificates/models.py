

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel


class CertificateModel(TimeStampedModel):
    id = models.UUIDField(
        'ID',
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        serialize=False,
        editable=False
    )

    name = models.CharField(
        _('Name'),
        max_length=100
    )

    document_number = models.CharField(
        _('Document number'),
        max_length=20,
        unique=True
    )
    
    step = models.IntegerField(
        _('Step'),
        default=1,
        help_text=_('Step of the certificate')
    )

    def masked_document_number(self):
        """Returns the ID number with all but the last four digits masked."""
        last_four = self.document_number[-4:]
        masked = '*' * (len(self.document_number) - 4) + last_four
        return masked
    
    def __str__(self):
        return f'{self.name} {self.masked_document_number()}'

    class Meta:
        db_table = "apps_project_specific_certificates_certificate"
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")
        ordering = ["default_order", "-created"]
        permissions = [
            ('view_certificate', 'Can view certificate list'),
        ]
