from .common import *

SECRET_KEY = 'django-insecure-gv9ea(a5%lcy3+z6dt^00z69j7k(q*p!$y$t^z1y4y_jsds59z'

DEBUG = True

ALLOWED_HOSTS = []

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]
