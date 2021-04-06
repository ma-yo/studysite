from .base import *
import datetime
import logging

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

DEBUG = False

PRODUCTION = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'studydb',
        'USER': 'redbee',
        'PASSWORD': 'w1x1y0z9',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_ROOT = '/home/redbee/www/html/web_app/studysite/trunc/static'

# will output to logging file
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = '/var/log/django/' + datetime.datetime.now().strftime('%Y%m%d') + '-server.log',
    filemode = 'a'
)