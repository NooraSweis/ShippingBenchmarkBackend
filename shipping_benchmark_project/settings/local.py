from .base import *

ENV = "Local"

# database configs

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'shipping_benchmark',
        'USER': os.environ['DB_USER_NAME'],
        'PASSWORD': os.environ['DB_PASSWORD']
    }
}

REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS': 'api_documentation.openapi.AutoSchema'}

SECRET_KEY = os.environ['SECRET_KEY']
