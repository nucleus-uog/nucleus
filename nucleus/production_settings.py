import os
from .settings import *

# Override settings for production.
DEBUG = False
SECRET_KEY = os.environ['NUCLEUS_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': os.environ['NUCLEUS_DB_USERNAME'],
        'PASSWORD': os.environ['NUCLEUS_DB_PASSWORD'],
        'HOST': os.environ['NUCLEUS_DB_HOST'],
        'PORT': os.environ['NUCLEUS_DB_PORT']
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (os.environ['NUCLEUS_REDIS_HOST'],
                 os.environ['NUCLEUS_REDIS_PORT'])
            ],
        },
    },
}