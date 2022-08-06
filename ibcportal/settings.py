import os
import environ
# import dj_database_url

import cloudinary  # cloudinary
import cloudinary.uploader  # cloudinary
import cloudinary.api  # cloudinary
import django_on_heroku
from datetime import timedelta

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('IBC_PORTAL_SECRET_KEY', '123')
# print(SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # libs and apis (third-party)
    'paypal.standard.ipn',
    'corsheaders',
    'rest_framework',
    # 'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'cloudinary',
    'import_export',
    # project apps
    'core',
    'groups',
    'ebd',
]

cloudinary.config(
    cloud_name=env('CLOUDINARY_CLOUD_NAME'),
    api_key=env('CLOUDINARY_API_KEY'),
    api_secret=env('CLOUDINARY_API_SECRET')
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'ibcportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'ibcportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME') or 'public',
        'USER': env('DATABASE_USER') or 'postgres',
        'PASSWORD': env('DATABASE_PASSWORD') or 'root',
        'HOST': env('DATABASE_HOST') or 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_ALLOW_ALL = False

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:8000',
# ]

# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:8000',
# )

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

JET_SIDE_MENU_COMPACT = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'media')
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

# Production database configuration
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

SECURE_PROXY_SSL_HEADER = ('https_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = 'ALLOW-FROM self'

# ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
# ALLOWED_HOSTS = ['ibcportal.herokuapp.com']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# PagSeguro Configuration
PAGSEGURO_TOKEN = os.getenv('IBC_PORTAL_PAGSEGURO_TOKEN', '123')
# print(PAGSEGURO_TOKEN)
PAGSEGURO_EMAIL = 'glenonsilva@gmail.com'
PAGSEGURO_SANDBOX = True

# Paypal Configuration
PAYPAL_TEST = True
PAYPAL_EMAIL = 'glenonsilva@gmail.com'

# Youtube API V3 Configuration
YOUTUBE_KEY = os.getenv('IBC_PORTAL_YOUTUBE_KEY', '123')
# print(YOUTUBE_KEY)
YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/videos'

# Firebase API Key (Chave do Servidor)
FIREBASE_KEY = os.getenv('FIREBASE_KEY', '123')

# JWT Config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}

# AWS Keys
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


django_on_heroku.settings(locals())