import os

from .base import *


CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'visualizer',
        'USER': os.environ['USER'],
    },
}
