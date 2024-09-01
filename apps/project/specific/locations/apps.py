from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.project.specific.locations'
    verbose_name = _("2. Location")
    verbose_name_plural = _("2. Locations")
