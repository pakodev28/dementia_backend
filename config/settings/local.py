from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-lk(u#t%wrk!_(q@*dn#!#l7z=pb6k+j^h8wwe2hdf%zb1+0b80'

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
