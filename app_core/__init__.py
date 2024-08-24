import re
import unicodedata

from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


def get_app_from_path(path):
    try:
        return import_string(path)
    except ImportError as e:
        raise ImproperlyConfigured(f'Can not import module from {path}: {e}')


def remove_accents(input_str:str):
    """
    Removes accents and special characters from the input string.
    Converts spaces to underscores.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    only_ascii = only_ascii.replace(' ', '_')
    cleaned_str = re.sub(r'[^a-zA-Z0-9_-]', '', only_ascii)
    return cleaned_str.lower()
