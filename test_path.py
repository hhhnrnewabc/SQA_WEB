
# LOGS
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASE_ROUTERS = ['mysite.dbsetings.AuthRouter', 'mysite.dbsetings.MasterSlaveRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


STATIC_URL = '/static/'
STATIC_ROOT = "./static/"
# STATICFILES_DIRS =("/var/www/example.com/media",)

MEDIA_URL = '/media/'
MEDIA_ROOT = "./media/"


# Testing mail
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025


# Error mail address
# The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
SERVER_EMAIL = 'sqa.web.service@gmail.com'

# When DEBUG=False and a view raises an exception,
# Django will email these people with the full exception information
# Each member of the tuple should be a tuple of (Full name, email address).
#
ADMINS = (
         ('Yu, Yen', 'hhhnrnew82@gmail.com'),
)
# Sends broken link notification emails to MANAGERS (see Error reporting).
# MANAGERS
