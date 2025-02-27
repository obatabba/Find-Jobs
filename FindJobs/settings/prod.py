import os
import dj_database_url
from .common import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS']

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL', ''))
}