from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel


class IPBlockedModel(TimeStampedModel):
    class ReasonsChoices(models.TextChoices):
        SERVER_HTTP_REQUEST = 'RA', _('Attempts to obtain forbidden urls')
        SECURITY_KEY_ATTEMPTS = 'SK', _(
            'Multiple failed security key entry attempts'
        )

    is_active = models.BooleanField(
        _("is blocked"),
        default=True
    )

    current_ip = models.CharField(
        _('current user ip'),
        max_length=150
    )

    reason = models.CharField(
        _("reason"),
        max_length=4,
        choices=ReasonsChoices.choices,
        default=ReasonsChoices.SERVER_HTTP_REQUEST
    )

    def __str__(self):
        return self.current_ip

    class Meta:
        db_table = 'apps_common_core_iptoblock'
        verbose_name = 'IP Blocked'
        verbose_name_plural = 'IPs Blocked'


auditlog.register(
    IPBlockedModel,
    serialize_data=True
)
