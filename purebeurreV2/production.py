from . import *
import raven

SECRET_KEY = '-~aO;| F;rE[??/w^zcumh(9'
DEBUG = False
ALLOWED_HOSTS = ['188.166.18.228','purbeurrev10.xyz']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # on utilise l'adaptateur postgresql
        'NAME': 'purbeurre_1208',  # le nom de notre base de donnees creee precedemment
        'USER': 'purbeurre32303138',  # attention : remplacez par votre nom d'utilisateur
        'PASSWORD': '@##Purebeurre2018##@',
        'HOST': '10.24.8.123',
        'PORT': '5432',
    }
}

INSTALLED_APPS += [
    	'raven.contrib.django.raven_compat',
]


RAVEN_CONFIG = {
   'dsn': 'https://226d019280ce4c61b455b8ea89ea9b67:87c5e1e1f00543e48b8a7379b4423e1b@sentry.io/1261690', # caution replace by your own!!
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    	'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),

}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO', # WARNING by default. Change this to capture more than warnings.
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
