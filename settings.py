DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEPLOYMENT_TIMESTAMP = 1358967866 

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'ml_enterprise',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 27017,
    }
}

CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION':'127.0.0.1:11211',
    }
}

SITE_HOST = 'ENTER_SITE_HOST'

STATIC_HOST = SITE_HOST

IMAGE_HOST = SITE_HOST

DYNAMIC_IMAGES_WEB_ROOT = '/static/CACHE/images/'

DYNAMIC_IMAGES_ROOT = '/usr/local/metaLayer-enterprise/enterprise/metalayercore/imaging/CACHE/'

THEMES_ROOT = '/usr/local/metaLayer-enterprise/enterprise/static/themes'

SENTRY_DSN = 'http://cb24eedee3b149c0966cb312dedcbd8c:598474230fe84813bfd9d0da84098d2e@108.166.111.61:9000/5'

TEMPLATE_DIRS = ( '/usr/local/metaLayer-enterprise/enterprise/static/html', )

SITE_URLS = {
    'company_prefix':'company'
}

AUTH_PROFILE_MODULE = "userprofiles.UserProfile"

INSIGHT_CATEGORIES = []

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = '/tmp/'
MEDIA_URL = ''

STATIC_ROOT = ''
STATIC_URL = '/static/'

SECRET_KEY = 'gh_uttm==e7005!ew!z5ae#&5)0nj_-*yx6659-ujc-0@4j68c'

FILE_UPLOAD_MAX_MEMORY_SIZE = 0

TEMPLATE_LOADERS = ( 'django.template.loaders.filesystem.Loader', )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "enterprise.contextprocessors.strings.context_strings",
    "enterprise.contextprocessors.themes.context_themes",
    "enterprise.contextprocessors.settings.context_settings",
    'enterprise.contextprocessors.company.context_company',
    'enterprise.contextprocessors.additionalhtml.context_additionalhtml',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'enterprise.middleware.devicedetection.DeviceDetectionMiddleware',
    'enterprise.middleware.companydetection.CompanyDetectionMiddleware',
)

ROOT_URLCONF = 'enterprise.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'enterprise.themanager',
    'enterprise.middleware',
    'enterprise.contextprocessors',
    'enterprise.userprofiles',
    'enterprise.customtags',
    'enterprise.emails',
    'enterprise.metalayercore.imaging',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
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


LOGIN_AND_REDIRECTION_POLICIES = [
    'superadminpolicy',
    'companymemberpolicy',
]

SOLR_PARAMS = 'wt=json&facet=on&sort=time+desc&rows=100&facet.mincount=1&stats=true'
SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://localhost:8080/solr',
    'solr_params': SOLR_PARAMS,
    'solr_facets':{},
    'solr_update_url':'update'
}

VISUALIZATIONS_CONFIG = {
    'visualization_display_hierarchy':[
        'googlegeochart',
        'd3cloud',
        'googlelinechart',
        'googlebarchart',
        'googlepiechart',
        'googleareachart'
    ]
}

GOOGLE_ANALYTICS = {
    'account':'',
    'site_host':'',
}

ADDITIONAL_PAGE_INCLUDES = [
    'getsatisfaction.html'
]

import socket
if socket.gethostname() in ['mattgriffiths', 'GRIFF-LINUX2']:
    from settings_matt import *
if socket.gethostname() in ['rich.dev.01']:
    from settings_rich import *
elif socket.gethostbyname(socket.gethostname()) in ['108.166.98.106']:
    from settings_dev import *
elif socket.gethostbyname(socket.gethostname()) in ['108.166.98.69']:
    from settings_clienttest import *
elif socket.gethostbyname(socket.gethostname()) in ['108.166.124.231']:
    from settings_prod_draftfcb import *
elif socket.gethostname() in ['delv.demo.01']:
    from settings_delvdemo import *
elif socket.gethostname() in ['me.prod.wwp.01']:
    from settings_prod_wwp import *
