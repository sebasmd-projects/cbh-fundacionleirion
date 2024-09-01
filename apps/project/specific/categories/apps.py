from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.project.specific.categories'
    verbose_name = _("0. Category")
    verbose_name_plural = _("0. Categories")
