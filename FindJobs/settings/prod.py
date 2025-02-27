import os
import dj_database_url
from .common import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

DATABASES = {
    'default': dj_database_url.parse(os.environ['DATABASE_URL'])
}