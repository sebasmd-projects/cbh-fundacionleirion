import hashlib

from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


def generate_md5_hash(value: str) -> str:
    """
    Generate an MD5 hash for the given value.
    """
    return hashlib.md5(value.encode('utf-8')).hexdigest()


def get_app_from_path(path):
    try:
        return import_string(path)
    except ImportError as e:
        raise ImproperlyConfigured(f'Can not import module from {path}: {e}')
