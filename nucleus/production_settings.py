import os
from .settings import *

# Override settings for production.
DEBUG = False
SECRET_KEY = os.environ['NUCLEUS_SECRET_KEY']

# Configure a mysql backend for the production
# configuration using environment variables.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['NUCLEUS_DB_NAME'],
        'USER': os.environ['NUCLEUS_DB_USERNAME'],
        'PASSWORD': os.environ['NUCLEUS_DB_PASSWORD'],
        'HOST': os.environ['NUCLEUS_DB_HOST'],
        'PORT': int(os.environ['NUCLEUS_DB_PORT'])
    }
}

# Configure a redis channels backend for the production
# configuration using environment variables.
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (os.environ['NUCLEUS_REDIS_HOST'],
                 int(os.environ['NUCLEUS_REDIS_PORT']))
            ],
        },
        "ROUTING": "nucleus_app.routes.channel_routing"
    },
}
