"""
Configurações de produção para Regional Veículos
"""

from .settings import *
import os
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Hosts permitidos em produção (substitua pelo seu domínio)
ALLOWED_HOSTS = [
    'regionalveiculos.com.br',
    'www.regionalveiculos.com.br', 
    'regionalveiculos.herokuapp.com',
    'localhost',
    '127.0.0.1'
]

# Database para produção (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='regional_veiculos_prod'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Configurações de Email para produção
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='contato@regionalveiculos.com.br')

# Configurações de segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
X_FRAME_OPTIONS = 'DENY'

# SSL/HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files para produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configurações de cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
    }
}

# Compressão e otimização
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# Logging para produção
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# IDs de Analytics (substitua pelos seus)
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')
FACEBOOK_PIXEL_ID = config('FACEBOOK_PIXEL_ID', default='')

# WhatsApp Business API
WHATSAPP_BUSINESS_NUMBER = config('WHATSAPP_BUSINESS_NUMBER', default='')
