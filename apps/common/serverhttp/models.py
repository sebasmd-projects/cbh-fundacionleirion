from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.utils.models import TimeStampedModel


class IPToBlockModel(TimeStampedModel):
    is_active = models.BooleanField(
        _("is blocked"),
        default=False
    )
    
    current_ip = models.CharField(
        _('current user ip'),
        max_length=150
    )

    def __str__(self):
        return self.current_ip

    class Meta:
        db_table = 'apps_common_serverhttp_iptoblock'
        verbose_name = 'IP To Block'
        verbose_name_plural = 'IPs To Block'
