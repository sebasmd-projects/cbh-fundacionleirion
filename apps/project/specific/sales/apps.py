from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.project.specific.sales'
    verbose_name = _("Sale")
    verbose_name_plural = _("Sales")
