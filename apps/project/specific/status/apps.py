from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class StatusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.project.specific.status'
    verbose_name = _("3. State")
    verbose_name_plural = _("3. Status")
