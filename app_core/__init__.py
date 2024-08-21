from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


def get_app_from_path(path):
    try:
        return import_string(path)
    except ImportError as e:
        raise ImproperlyConfigured(f'Can not import module from {path}: {e}')
