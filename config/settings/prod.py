# flake8: noqa
from .base import *

DEBUG = False

SECRET_KEY = 'django-insecure-lk(u#t%wrk!_(q@*dn#!#l7z=pb6k+j^h8wwe2hdf%zb1+0b80'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
