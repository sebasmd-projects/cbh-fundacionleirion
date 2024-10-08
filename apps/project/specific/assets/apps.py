from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BondsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.project.specific.assets'
    verbose_name = _("1. Asset")
    verbose_name_plural = _("1. Assets")
