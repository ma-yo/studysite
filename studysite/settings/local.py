from .base import *
import logging

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'studydb',
        'USER': 'redbee',
        'PASSWORD': 'w1x1y0z9',
        'HOST': '192.168.0.200',
        'PORT': '3306',
    }
}

# will output to your console
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
)