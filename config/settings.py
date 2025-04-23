import os
from pathlib import Path
from decouple import config
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG') == 'True'
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')


# Application definition
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'rest_framework',
    'djoser',
    'social_django',
    'corsheaders',
    'storages',
    'django_summernote',
    'crispy_forms',
    'crispy_tailwind',

    # apps...
    'core.apps.CoreConfig',
    'apps.platform.accounts.apps.AccountsConfig',
    'apps.platform.workspace.apps.WorkspaceConfig',
]


# CORS settings
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS').split(',')
CORS_ALLOW_CREDENTIALS = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']


# Rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'config.middlewares.CustomLocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middlewares.RedirectAuthenticatedMiddleware',
]


AUTH_USER_MODEL = 'core.User'
ROOT_URLCONF = 'config.urls'


# Base settings
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Messages settings
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

MESSAGE_TAGS = {
    messages.SUCCESS: 'bg-green-50 text-green-500',
    messages.WARNING: 'bg-amber-50 text-amber-500',
    messages.ERROR: 'bg-red-50 text-red-500',
}


WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_USER_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
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
LANGUAGES = (
    ('kk', _('Kazakh')),
    ('ru', _('Russian')),
    ('en', _('English')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'kk'
MODELTRANSLATION_LANGUAGES = ('kk', 'ru', 'en', )

MODELTRANSLATION_TRANSLATION_FILES = (
    'core.translations',
)

LOCALE_PATHS = [
    BASE_DIR / 'locales'
]

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
if DEBUG:
    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STORAGES = {
        'default': {
            'BACKEND': 'config.storages.MediaStore',
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
        },
    }

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates/static')
]


# Crispy settings
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email settings
# ----------------------------------------------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True


# Simple JWT settings
# ----------------------------------------------------------------------------------------------------------------------
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'BLACKLIST_AFTER_ROTATION': False,
}


# Domain
DOMAIN = config('DOMAIN')
SITE_NAME = config('SITE_NAME')


# Djoser settings
# ----------------------------------------------------------------------------------------------------------------------
DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_RESET_CONFIRM_URL': 'auth/password/reset/confirm/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'USERNAME_RESET_CONFIRM_URL': 'auth/username/reset/confirm/{uid}/{token}',

    'SERIALIZERS': {
        'user_create': 'core.serializers.UserSerializer',
        'user': 'core.serializers.UserSerializer',
        'current_user': 'core.serializers.UserAccountSerializer',
        'user_delete': 'djoser.serializers.UserSerializer',
    },

    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': config('REDIRECT_URLS').split(','),
}


# OAuth2 Google
# ----------------------------------------------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile', 'openid']
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    ('given_name', 'first_name'),
    ('family_name', 'last_name'),
    ('picture', 'google_avatar'),
    ('email', 'email'),
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'core.pipelines.update_google_avatar',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
