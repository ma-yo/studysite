from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
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
    filename = '/var/log/django/server.log',
    filemode = 'a'
)