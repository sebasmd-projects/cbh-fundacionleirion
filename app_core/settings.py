import base64
import logging
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from import_export.formats.base_formats import CSV, HTML, JSON, TSV, XLS, XLSX

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(
    filename='stderr.log', format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'
)

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if os.getenv('DJANGO_DEBUG') == 'True':
    DEBUG = True
else:
    DEBUG = False

if os.getenv('DJANGO_SECURE_SSL_REDIRECT') == 'True':
    SECURE_SSL_REDIRECT = True
else:
    SECURE_SSL_REDIRECT = False

if ',' in os.getenv('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = [os.getenv('DJANGO_ALLOWED_HOSTS')]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'auditlog',
    'import_export',
    'parler',
    'rosetta',
]

CUSTOM_APPS = [
    'apps.common.core',
    'apps.common.serverhttp',
    'apps.common.utils',

    'apps.project.common.account',
    'apps.project.common.notifications',
    'apps.project.common.reports',
    'apps.project.common.users',

    'apps.project.specific.assets',
    'apps.project.specific.categories',
    'apps.project.specific.certificates',
    'apps.project.specific.locations',
    'apps.project.specific.sales',
    'apps.project.specific.status',
]

ALL_CUSTOM_APPS = CUSTOM_APPS

if DEBUG:
    INSTALLED_APPS = THIRD_PARTY_APPS + ALL_CUSTOM_APPS + DJANGO_APPS
else:
    INSTALLED_APPS = THIRD_PARTY_APPS + ALL_CUSTOM_APPS + DJANGO_APPS

IMPORT_EXPORT_FORMATS = [CSV, HTML, JSON, TSV, XLS, XLSX]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 6000

LOCALE_PATHS = [
    app_path / 'locale' for app_path in [BASE_DIR / app.replace('.', '/') for app in ALL_CUSTOM_APPS]
]

LOCALE_PATHS.append(str(BASE_DIR / 'app_core' / 'locale'))

UTILS_PATH = 'apps.common.utils'

ADMIN_URL = os.getenv('DJANGO_ADMIN_URL')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.common.utils.middleware.RedirectWWWMiddleware',
    'apps.common.utils.middleware.BlockIPMiddleware',
]

MIDDLEWARE_NOT_INCLUDE = [os.getenv('MIDDLEWARE_NOT_INCLUDE')]

ROOT_URLCONF = 'app_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                f'{UTILS_PATH}.context_processors.custom_processors'
            ],
        },
    },
]

WSGI_APPLICATION = 'app_core.wsgi.application'

DATABASES = {
    'default': {
        'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE')),
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': int(os.getenv('DB_PORT')),
        'CHARSET': os.getenv('DB_CHARSET'),
        'ATOMIC_REQUESTS': True
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.UserModel'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    f'{UTILS_PATH}.backend.EmailOrUsernameModelBackend',
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

ENCODED_KEY = base64.urlsafe_b64encode(SECRET_KEY[:32].encode('utf-8'))

MAX_KEY_ATTEMPS = os.getenv('MAX_KEY_ATTEMPS')

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_AGE = 7200

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English')
]

PARLER_LANGUAGES = {
    None: (
        {'code': 'es', },
        {'code': 'en', },
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}

ROSETTA_SHOW_AT_ADMIN_PANEL = True

STATIC_URL = '/static/'

STATIC_ROOT = str(os.getenv('DJANGO_STATIC_ROOT'))

MEDIA_URL = '/media/'

MEDIA_ROOT = str(os.getenv('DJANGO_MEDIA_ROOT'))

STATICFILES_DIRS = [str(BASE_DIR / 'public' / 'staticfiles')]

# subdomains/controlbonoshistoricos/public

if bool(os.getenv('DJANGO_EMAIL_USE_SSL')):
    EMAIL_USE_SSL = True
    EMAIL_USE_TLS = False
else:
    EMAIL_USE_SSL = False
    EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = os.getenv('DJANGO_EMAIL_DEFAULT_FROM_EMAIL')
EMAIL_BACKEND = os.getenv('DJANGO_EMAIL_BACKEND')
EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', 'mail.fundacionleirion.com')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER')
EMAIL_PORT = int(os.getenv('DJANGO_EMAIL_PORT'))


EDIT_USER_GROUP = os.getenv('PERMISSION_EDIT_USER_GROUP')
EDIT_USERS_GROUP = os.getenv('PERMISSION_EDIT_USERS_GROUP')
EDIT_ASSETS_STATUS_REFERENCE = os.getenv(
    'PERMISSION_EDIT_ASSETS_STATUS_REFERENCE'
)
EDIT_ASSETS_LOCATION = os.getenv('PERMISSION_EDIT_ASSETS_LOCATION')

SALES_GROUP = os.getenv('PERMISSION_SALES_GROUP')
KEY_BYPASS_GROUP = os.getenv('PERMISSION_KEY_BYPASS_GROUP')
