import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

from django_drf_boilerplate.utils.env_validate import validate_env

BASE_DIR = Path(__file__).resolve().parent.parent

# load env variables
load_dotenv()

# If you have any environment variables that are required, you can add them to the list below
required_env_vars = ['DJANGO_SECRET',  'DB_NAME',
                     'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'CACHE_URL']
validate_env(required_env_vars)

# function to validate the environment variables are set and that they are not empty


DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']  # allow only your domain to access the API
SECRET_KEY = os.getenv('DJANGO_SECRET')

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv('CACHE_URL'),
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=2),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
