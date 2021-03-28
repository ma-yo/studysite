from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j_z=6n3bh8(yghg)+h9e-)ca6k6%51%jtz6zux8(mhy3+#!eiu'

# SECURITY WARNING: don't run with debug turned on in production!
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