from settings import SOLR_PARAMS

DEBUG = True

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://108.166.59.173:8080/solr',
    'solr_params':SOLR_PARAMS,
    'solr_facets':{}
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

SENTRY_DSN = 'http://cb24eedee3b149c0966cb312dedcbd8c:598474230fe84813bfd9d0da84098d2e@108.166.111.61:9000/5'

TEMPLATE_DIRS = ( '/home/rich/metaLayer-enterprise/enterprise/static/html', )

STATICFILES_DIRS = ( '/home/rich/metaLayer-enterprise/enterprise/static/', )

STATICFILES_FINDERS = ( 'django.contrib.staticfiles.finders.FileSystemFinder', )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
        },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
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
