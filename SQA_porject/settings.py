"""
Django settings for SQA_porject project.

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/Library/Logs/django/SQA_porject/debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

ALLOWED_HOSTS = []


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
    'steam',
    'baseuser',
    'django_nose',  #django nose for testing

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'SQA_porject.urls'

WSGI_APPLICATION = 'SQA_porject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'django_SQA_porject_Auth',
       'USER': 'swim',
       'PASSWORD': '1314',
       'HOST': '127.0.0.1',
       'PORT': '3306'
    },

   'mariadb': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'django_SQA_porject',
       'USER': 'swim',
       'PASSWORD': '1314',
       'HOST': '127.0.0.1',
       'PORT': '3306'
    },
}

# DATABASE_ROUTERS = ['mysite.dbsetings.AuthRouter', 'mysite.dbsetings.MasterSlaveRouter']

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'zh-tw'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "/var/www/swim-fish.twbbs.org/static/"
# STATICFILES_DIRS =("/var/www/example.com/media",)

MEDIA_URL = '/media/'
MEDIA_ROOT = "/var/www/swim-fish.twbbs.orgmedia/"

# #SSL
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_USER_MODEL = 'baseuser.BaseUser'

#django nose testing setting
# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'baseuser' apps
NOSE_ARGS = [
    '--with-coverage',
    # '--cover-erase',
    '--cover-tests',
    '--cover-package=baseuser',
    '--cover-html',

]
