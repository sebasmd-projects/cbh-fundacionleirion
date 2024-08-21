import logging
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

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
    'rosetta'
]

CUSTOM_APPS = [
    'apps.common.utils',
    'apps.common.serverhttp',

    'apps.project.common.users',
]

ALL_CUSTOM_APPS = CUSTOM_APPS

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + ALL_CUSTOM_APPS

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
    'apps.common.utils.middleware.APILogMiddleware',
]

MIDDLEWARE_NOT_INCLUDE = [os.getenv('MIDDLEWARE_NOT_INCLUDE')]

ROOT_URLCONF = 'app_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'apps'],
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

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_AGE = 7200

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English'))
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

EMAIL_BACKEND = os.getenv('DJANGO_EMAIL_BACKEND')
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', 'mail.fundacionleirion.com')
EMAIL_PORT = int(os.getenv('DJANGO_EMAIL_PORT'))
DEFAULT_FROM_EMAIL = os.getenv('DJANGO_EMAIL_DEFAULT_FROM_EMAIL')
