from . import *
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # on utilise l'adaptateur postgresql
        'NAME': 'test_db',  # le nom de notre base de donnees creee precedemment
        'USER': 'postgres',  # attention : remplacez par votre nom d'utilisateur
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}