import os

from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'visualizer',
        'USER': os.environ['USER'],
    },
}
