from .base import *


def read_secret(secret_name):
    
    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.strip()
    file.close()

    return secret


DEBUG = False


BASE_BACKEND_URL = env.str('DJANGO_BASE_BACKEND_URL')
BASE_FRONTEND_URL = env.str('DJANGO_BASE_FRONTEND_URL')


# CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = env.list(
#     'DJANGO_CORS_ORIGIN_WHITELIST',
#     default=[BASE_FRONTEND_URL]
# )

# 실제 배포시 바꿀 예정
ALLOWED_HOSTS = ['buscp.org']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'projectdb',
        'USER': 'project',
        'PASSWORD': read_secret('PROJECT_MARIADB_PASSWORD'),
        'HOST': 'projectmariadb',
        'PORT': '3306',
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000


