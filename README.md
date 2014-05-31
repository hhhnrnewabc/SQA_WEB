SQA PROJECT WEB
===============

[![Build Status](https://travis-ci.org/hhhnrnewabc/SQA_WEB.svg?branch=master)](https://travis-ci.org/hhhnrnewabc/SQA_WEB)
[![Coverage Status](https://coveralls.io/repos/hhhnrnewabc/SQA_WEB/badge.png?branch=master)](https://coveralls.io/r/hhhnrnewabc/SQA_WEB?branch=master)

INSTALLING THE PKG
------------------

####This PROJECT relies on the GNU gettext toolset.

#####Using apt-get:

    sudo apt-get install gettext


####Using pip:

    pip install -q pillow
    pip install -q Django==1.6.5
    
    pip install pymysql
    pip install djangorestframework
    pip install markdown
    pip install django-filter
    pip install django-bootstrap-form
    pip install pytz
    pip install django-taggit
    pip install django-grappelli
    pip install south
    
####For test (coveralls.io):

    pip install -q coveralls
    pip install -q coverage
    pip install django-nose


####Not use SSL

in `SQA_Project.settings`

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

Comment it out 
   