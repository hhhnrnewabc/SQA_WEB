"""
Django settings for SQA_Project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=j*!hhle^wxqgs$12o&2rg2$mhl7*+tqy7o#f%@k7*6o7dzt2%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


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
    'baseuser',
    'steam',
    'steam_dev',
    'steam_user',
    'django_nose',  # django nose testing
    'bootstrapform',  # Twitter Bootstrap for Django Form.

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 自動切換語言
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'baseuser.middleware.time_zone.TimezoneMiddleware',  # for change time_zone
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Django Debug Toolbar
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",  # tags need
)

ROOT_URLCONF = 'SQA_Project.urls'

WSGI_APPLICATION = 'SQA_Project.wsgi.application'




# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-tw'

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
            ('en', _("English (English)")),
            ('zh-tw', _("Traditional Chinese (繁體中文)")),
            ('ja', _("Japanese (日本語)")),
)

LOCALE_PATHS = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale'),
)

TIME_ZONE = 'UTC'
# TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/



# #SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_USER_MODEL = 'baseuser.BaseUser'

#django nose testing setting
# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'baseuser' apps
NOSE_ARGS = [
    '--with-coverage',
    # '--cover-erase',
    '--cover-tests',
    '--cover-package=baseuser, steam,steam_user,steam_dev',
    '--cover-html',
]

# for bootstrap3 class
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

NO_IMAGE_AVAILABLE_PHOTO = 'noImageAvailable300.png'


# The number of days a signup link is valid for.
SIGNUP_TIMEOUT_DAYS = 7


# define auto load templatetags
AUTOLOAD_TEMPLATETAGS = (
    'bootstrapform.templatetags.bootstrap',
)

# for every template page load {% load i18n %}...
from django.template import add_to_builtins
add_to_builtins('django.templatetags.i18n')
add_to_builtins('django.contrib.staticfiles.templatetags.staticfiles')
for tag in AUTOLOAD_TEMPLATETAGS:
    add_to_builtins(tag)



# import path for AWS EC2 SERVER
# . is point to WEB/
# path put in ../aws_path_fix.py
import sys
sys.path.insert(0, '..')
from aws_path_fix import *
