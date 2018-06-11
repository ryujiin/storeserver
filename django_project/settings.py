"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import config
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'sorl.thumbnail',
    'paypal.standard.ipn',
    'ubigeo', 
    'corsheaders',
    'comentario',
    'carro',
    'catalogo',
    'cliente',
    'custom',
    'cmsweb',
    'pedido',
    'pago',
    'utiles',
    'backoffice.ofcatalogo',
    'backoffice.compra',
    'backoffice.contabilidad',
    'backoffice.cuenta',
    'backoffice.inventario',
    'backoffice.produccion',
    'backoffice.venta',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.name,
        'USER': config.user,
        'PASSWORD': config.password,
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = location('public/static')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    location('static/'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = location("public/media")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Allow Django from all hosts. This snippet is installed from
# /var/lib/digitalocean/allow_hosts.py

import os
import netifaces

# Find out what the IP addresses are at run time
# This is necessary because otherwise Gunicorn will reject the connections
def ip_addresses():
    ip_list = ['*']
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        for x in (netifaces.AF_INET, netifaces.AF_INET6):
            if x in addrs:
                ip_list.append(addrs[x][0]['addr'])
    return ip_list

# Discover our IP address
ALLOWED_HOSTS = ip_addresses()

CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
)
CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

AUTHENTICATION_BACKENDS = (
    'cliente.backends.EmailOrUsernameModelBackend',    
    'django.contrib.auth.backends.ModelBackend',
)

SHOP_CURRENCY = 'PEN'

#Paypal IPN
PAYPAL_RECEIVER_EMAIL = "ryujiin22@gmail.com"
PAYPAL_TEST = False
PAYPAL_URL_FRONT_RETURN = '//lovizdc.com/gracias/'
PAYPAL_URL_CANCEL_RETURN = '//lovizdc.com/checkout/'
API_CURRENCY = config.API_CURRENCY

#Mercado Pago
CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET =  config.CLIENT_SECRET
MERCADO_PAGO_FAIL = 'https://lovizdc.com/checkout/'

URL = 'https://apiloviz.herokuapp.com'

#STripe
STRIPE_SECRET_KEY = config.STRIPE_SECRET_KEY

# Amzon s3

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY

AWS_STORAGE_BUCKET_NAME = 'lovizdc'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    location('static'),
]

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'api.storage_backends.MediaStorage'

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=7200),
}
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {},
    'EMAIL': {
        'password_reset': 'cliente.emails.PasswordResetEmail'
    }
}

EMAIL_HOST_USER = 'lovizdc'
EMAIL_HOST= 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = 'C4b4ll0s'

DEFAULT_FROM_EMAIL = 'admin@lovizdc.com'

DOMAIN = 'lovizdc.com'
SITE_NAME = 'Loviz DelCarpio'

UNIDADES = (
    ('und','Unidad'),
    ('par','Par'),
    ('fr','Fardo'),
    ('pq','Paquete'),
    ('m','Metros'),
    ('cm','Centimetros'),
)

try:
    from .local import *
except ImportError:
    pass