import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

load_dotenv()

#PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
#DEVELOPMENT = os.getenv('DEVELOPMENT', 'False').lower() in ('true', '1', 't')


ALLOWED_HOSTS = [str(os.getenv('ALLOWED_HOSTS'))]


# Application definition

INSTALLED_APPS = [
    'account',
    'doctor',
    'patient',
    'invoice',
    'dashboard',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'taggit',
    'modelcluster',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE += ('crum.CurrentRequestUserMiddleware',)
MIDDLEWARE += ('wagtail.contrib.redirects.middleware.RedirectMiddleware',)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': str(os.getenv('DB_ENGINE')),
        'NAME': str(os.getenv('DB_NAME')),
        'USER': str(os.getenv('DB_USER')),
        'PASSWORD': str(os.getenv('DB_PASSWORD')),
        'HOST': str(os.getenv('DB_HOST')),
        'PORT': str(os.getenv('DB_PORT')),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'id-id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = False
#WAGTAIL_I18N_ENABLED = True

USE_TZ = True

USE_L10N = False


USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'
#DATE_FORMAT = 'j N Y'
#DATE_INPUT_FORMATS = 'd-m-Y'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

#STATICFILES_DIRS = [
#    os.path.join(PROJECT_DIR, 'static'),
#]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'


ADMINS = [
    # ('Your Name', 'your_email@example.com'),
]
MANAGERS = ADMINS

# Default to dummy email backend. Configure dev/production/local backend
# as per https://docs.djangoproject.com/en/stable/topics/email/#email-backends
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


EMAIL_SUBJECT_PREFIX = '[CarePlus] '

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/stable/topics/logging for
# more details on how to customise your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# WAGTAIL SETTINGS

#WAGTAILADMIN_BASE_URL = 'https://dental.careplus.cloud'
WAGTAILADMIN_BASE_URL = str(os.getenv(('WAGTAILADMIN_BASE_URL')))
# This is the human-readable name of your Wagtail install
# which welcomes users upon login to the Wagtail admin.
WAGTAIL_SITE_NAME = 'CarePlus THT'

#WAGTAIL_DATE_FORMAT = '%d-%m-%Y'
#WAGTAIL_DATETIME_FORMAT = '%d-%m-%Y %H:%M'
#WAGTAIL_TIME_FORMAT = '%H:%M'
WAGTAIL_PASSWORD_RESET_ENABLED = False
WAGTAIL_GRAVATAR_PROVIDER_URL = '//www.gravatar.com/avatar'
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'noreply@careplus.cloud'

# CSRF
CSRF_TRUSTED_ORIGINS = [WAGTAILADMIN_BASE_URL]

# Replace the search backend
#WAGTAILSEARCH_BACKENDS = {
#  'default': {
#    'BACKEND': 'wagtail.search.backends.elasticsearch5',
#    'INDEX': 'myapp'
#  }
#}

# Wagtail email notifications from address
# WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'wagtail@myhost.io'

# Wagtail email notification format
# WAGTAILADMIN_NOTIFICATION_USE_HTML = True

# Reverse the default case-sensitive handling of tags
TAGGIT_CASE_INSENSITIVE = True

#SE_THOUSAND_SEPARATOR = True

#LANGUAGES = WAGTAIL_CONTENT_LANGUAGES = [
#    ('en-us', _("English")),
#    ('id-id', _("Indonesia")),
#]

# Email
EMAIL_BACKEND = str(os.getenv(('EMAIL_BACKEND')))
EMAIL_HOST = str(os.getenv(('EMAIL_HOST')))
EMAIL_PORT = os.getenv(('EMAIL_PORT'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = str(os.getenv(('EMAIL_HOST_USER')))
EMAIL_HOST_PASSWORD = str(os.getenv(('EMAIL_HOST_PASSWORD')))

# Account
AUTH_USER_MODEL = 'account.User'

WAGTAIL_USER_EDIT_FORM = 'account.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'account.forms.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['phone', 'address', 'membership']


WAGTAILADMIN_PERMITTED_LANGUAGES = []
WAGTAIL_USER_TIME_ZONES = []
