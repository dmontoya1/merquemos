# -*- coding: utf-8 -*-

import os
import raven
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = 'e^45&1bd1c5sr1_4yk&p@9r-f@pp#qe3b7)7uy27u094t8s1pq'

DEBUG = False

ALLOWED_HOSTS = [
    '34.231.240.208',
    'www.merquemos.co',
    'merquemos.co'
]

# Application definition
DJANGO_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
]

THIRD_PARTY_APPS = [
    'import_export',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_framework_docs',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'rest_auth.registration',
    'raven.contrib.django.raven_compat',
    'fcm_django',
    'adjacent',
    'easy_pdf',
]

PROJECT_APPS = [
    'api',
    'manager',
    'stock',
    'users',
    'sales',
    'reports',
    'utils',
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
    'django.contrib.sessions.middleware.SessionMiddleware'
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
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'
AUTHENTICATION_BACKENDS = (
   "django.contrib.auth.backends.ModelBackend",
   "allauth.account.auth_backends.AuthenticationBackend"
)
LOGIN_REDIRECT_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'
LOGOUT_ON_PASSWORD_CHANGE = True
OLD_PASSWORD_FIELD_ENABLED = True

#Social account settings
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'https'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'first_name',
            'last_name'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'es_CO',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.10'
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_ADAPTER = 'users.adapters.SocialAccountAdapter'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'merquemos',
        'USER': 'postgres',
        'PASSWORD': 'PkvdQWIfeNvg647',
        'HOST': 'localhost',
        'PORT': '5432',
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
STATIC_ROOT = '/var/www/merquemos.co/static/'


# User uploades files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/merquemos.co/media/'
FILE_UPLOAD_PERMISSIONS = 0644

# Email config
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'


# Sentry Config
RAVEN_CONFIG = {
    'dsn': 'https://e7a3800d1f6546d2999e3a658ba1d405:e8e87c77e875489c8531b6b67f397ed8@sentry.apptitud.com.co/5',
    'release': raven.fetch_git_sha(BASE_DIR),
}

# DRF Config
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

# FCM Config
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AIzaSyA103iO1CMBzGnUGhk1M2kp0iWK0ReUoyE"
}

#Centrifugo Config
CENTRIFUGE_ADDRESS = 'http://www.merquemos.co/centrifugo/'
CENTRIFUGE_SECRET = 'f@pp#qe3b7)7uy27u094t8s1pq'
CENTRIFUGE_TIMEOUT = 10

JET_INDEX_DASHBOARD = 'dashboard.IndexDashboard'