from .base import *


def read_secret(secret_name):
    
    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.strip()
    file.close()

    return secret


DEBUG = False

# 실제 배포시 바꿀 예정
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'projectdb',
        'USER': 'project',
        'PASSWORD': read_secret('PROJECT_MARIADB_PASSWORD'),
        'HOST': 'projectdb',
        'PORT': '3306',
    }
}
