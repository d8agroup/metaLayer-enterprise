from settings import SOLR_PARAMS

DEBUG = True

SOLR_CONFIG = {
    'default_page_size':100,
    #'solr_url':'http://localhost:8983/solr/collection1',
    'solr_url':'http://me.dev:8080/solr4',
    'solr_params':SOLR_PARAMS,
    'solr_facets':{},
    'solr_update_url':'update'
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@metalayer.com'
EMAIL_HOST_PASSWORD = '##M3taM3ta'
EMAIL_PORT = 587

SITE_HOST = 'localhost:8000'

STATIC_HOST = SITE_HOST

IMAGE_HOST = SITE_HOST

DYNAMIC_IMAGES_WEB_ROOT = '/static/CACHE/images/'

DYNAMIC_IMAGES_ROOT = '/home/matt/code/metaLayer/enterprise/metalayercore/imaging/CACHE/'

THEMES_ROOT = '/home/matt/code/metaLayer/enterprise/static/themes'

SENTRY_DSN = 'http://cb24eedee3b149c0966cb312dedcbd8c:598474230fe84813bfd9d0da84098d2e@108.166.111.61:9000/5'

TEMPLATE_DIRS = ( '/home/matt/code/metaLayer/enterprise/static/html', )

STATICFILES_DIRS = ( '/home/matt/code/metaLayer/enterprise/static/', )

STATICFILES_FINDERS = ( 'django.contrib.staticfiles.finders.FileSystemFinder', )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'WARNING',
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

OAUTH2_SETTINGS = {
    'GoogleOauth2Controller':{
        'client_id':'450032264506.apps.googleusercontent.com',
        'client_secret':'Pu-Fk1rPYFKATskh9ws1DTPI',
        'redirect_uri':'http://%s/oauth2/google_oauth2_callback' % SITE_HOST
    },
    'FacebookOauth2Controller': {
        'client_id': '457768257589473',
        'client_secret': 'd93ba13ce81f2f578f345865aaea2269',
        'redirect_uri':'http://%s/oauth2/facebook_oauth2_callback' % SITE_HOST
    }
}