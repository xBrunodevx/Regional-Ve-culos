"""
Regional Veículos - Production Settings
Professional Django configuration for production environment
"""

import os
import sys
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

def get_environment_variable(var_name, default=None, required=True):
    """
    Get environment variable or raise exception
    """
    try:
        return os.environ[var_name]
    except KeyError:
        if required and default is None:
            error_msg = f'The environment variable {var_name} is required'
            raise ImproperlyConfigured(error_msg)
        return default

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_environment_variable('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_environment_variable('DEBUG', 'False').lower() == 'true'

# Production domain configuration
ALLOWED_HOSTS = [
    'regionalveiculos.com.br',
    'www.regionalveiculos.com.br',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

# Add development hosts if DEBUG is True
if DEBUG:
    ALLOWED_HOSTS.extend([
        '*.localhost',
        '*.127.0.0.1',
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16',
    ])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    # Add third-party apps here when needed
    # 'rest_framework',
    # 'corsheaders',
    # 'crispy_forms',
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'contato.apps.ContatoConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'regional_veiculos.urls'

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
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'regional_veiculos.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_environment_variable('DB_NAME', 'regional_veiculos_prod'),
        'USER': get_environment_variable('DB_USER', 'postgres'),
        'PASSWORD': get_environment_variable('DB_PASSWORD'),
        'HOST': get_environment_variable('DB_HOST', 'localhost'),
        'PORT': get_environment_variable('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 20,
            'options': '-c default_transaction_isolation=serializable'
        },
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }
}

# SQLite fallback for development
if DEBUG and get_environment_variable('USE_SQLITE', 'False').lower() == 'true':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': get_environment_variable('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'KEY_PREFIX': 'regional_veiculos',
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Fallback to database cache for development
if DEBUG and get_environment_variable('USE_DB_CACHE', 'False').lower() == 'true':
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_environment_variable('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(get_environment_variable('EMAIL_PORT', '587'))
EMAIL_HOST_USER = get_environment_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_environment_variable('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = get_environment_variable('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = get_environment_variable('EMAIL_USE_SSL', 'False').lower() == 'true'

DEFAULT_FROM_EMAIL = get_environment_variable('DEFAULT_FROM_EMAIL', 'contato@regionalveiculos.com.br')
SERVER_EMAIL = get_environment_variable('SERVER_EMAIL', 'server@regionalveiculos.com.br')

# Email fallback for development
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Security Settings
if not DEBUG:
    # HTTPS/SSL Configuration
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Security Headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Session Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 3600  # 1 hour
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    
    # CSRF Security
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_TRUSTED_ORIGINS = [
        'https://regionalveiculos.com.br',
        'https://www.regionalveiculos.com.br',
    ]
    
    # Clickjacking Protection
    X_FRAME_OPTIONS = 'DENY'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'regional_veiculos': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# Create logs directory if it doesn't exist
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# Admin Configuration
ADMINS = [
    ('Admin', get_environment_variable('ADMIN_EMAIL', 'admin@regionalveiculos.com.br')),
]
MANAGERS = ADMINS

# File Upload Configuration
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# Performance Settings
if not DEBUG:
    # Database connection pooling
    DATABASES['default']['OPTIONS'].update({
        'MAX_CONNS': 20,
        'OPTIONS': {
            'MAX_CONNS': 20,
            'charset': 'utf8mb4',
        }
    })

# Custom Settings for Regional Veículos
SITE_NAME = 'Regional Veículos'
SITE_DESCRIPTION = 'Carros seminovos com qualidade e garantia'
COMPANY_NAME = 'Regional Veículos Ltda'
COMPANY_EMAIL = 'contato@regionalveiculos.com.br'
COMPANY_PHONE = '(11) 1234-5678'
COMPANY_ADDRESS = 'São Paulo, SP'

# Pagination
PAGINATE_BY = 12
MAX_PAGINATE_BY = 50

# Search Configuration
MIN_SEARCH_LENGTH = 3
MAX_SEARCH_RESULTS = 100

# Image Processing
MAX_IMAGE_SIZE = 2048  # pixels
IMAGE_QUALITY = 85
THUMBNAIL_SIZE = (300, 200)

# WhatsApp Integration
WHATSAPP_NUMBER = get_environment_variable('WHATSAPP_NUMBER', '5511987654321')
WHATSAPP_API_KEY = get_environment_variable('WHATSAPP_API_KEY', required=False)

# Google Services (optional)
GOOGLE_ANALYTICS_ID = get_environment_variable('GOOGLE_ANALYTICS_ID', required=False)
GOOGLE_MAPS_API_KEY = get_environment_variable('GOOGLE_MAPS_API_KEY', required=False)
GOOGLE_RECAPTCHA_PUBLIC_KEY = get_environment_variable('GOOGLE_RECAPTCHA_PUBLIC_KEY', required=False)
GOOGLE_RECAPTCHA_PRIVATE_KEY = get_environment_variable('GOOGLE_RECAPTCHA_PRIVATE_KEY', required=False)

# Development Tools
if DEBUG:
    # Django Debug Toolbar (if installed)
    if 'debug_toolbar' in sys.modules:
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1', '::1']
    
    # Django Extensions (if installed)
    if 'django_extensions' in sys.modules:
        INSTALLED_APPS.append('django_extensions')

# Message Framework
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Session Configuration
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_NAME = 'regional_veiculos_sessionid'

# CSRF Configuration
CSRF_COOKIE_NAME = 'regional_veiculos_csrftoken'

# API Configuration (for future use)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
