# -*- coding: utf-8 -*-

import os
import raven
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = 'e^45&1bd1c5sr1_4yk&p@9r-f@pp#qe3b7)7uy27u094t8s1pq'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
DJANGO_APPS = [
    'material', #Third party app, needs to be before django.contrib.admin
    'material.admin', #Third party app, needs to be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_framework_docs',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'raven.contrib.django.raven_compat',
    'fcm_django'
]

PROJECT_APPS = [
    'api',
    'manager',
    'stock',
    'users',
    'sales',
    'reports',
    'webclient'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'merquemos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'merquemos/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webclient.context_processors.webclient_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'merquemos.wsgi.application'

SITE_ID = 1

# Auth settings
AUTH_USER_MODEL = 'users.User'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'
AUTHENTICATION_BACKENDS = (
   "django.contrib.auth.backends.ModelBackend",
   "allauth.account.auth_backends.AuthenticationBackend"
)


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'merquemos',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "merquemos/static")
]


#User uploades files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, "merquemos/media")


#Email config
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'


#Sentry Config
RAVEN_CONFIG = {
    'dsn': 'https://79c7c7b847f144ac806773d761810fd9:17bde4d4addb4494b1e8a32f2aed91a3@sentry.io/210686',
    'release': raven.fetch_git_sha(BASE_DIR),
}

#DRF Config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.HasAPIAccess',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer'
}

#FCM Config
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAXfLtBHk:APA91bE-Wuu-aIiZjJFbJ7f_gRC3gZ77w7jGW-3bHxUFx3uaELBj91a3QDJ7uMnlAiSZprOTkgSfq8X2zmAvqkC2OdeOs5y7KCKVaZP4zeF3aV6K2FxegovhvkTnGkBsFcxIUC-EZoxD"
}
