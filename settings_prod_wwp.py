from settings import SOLR_PARAMS

DEBUG = False

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@metalayer.com'
EMAIL_HOST_PASSWORD = '##M3taM3ta'
EMAIL_PORT = 587

SITE_HOST = 'wwp.metalayer.com'

STATIC_HOST = SITE_HOST

IMAGE_HOST = SITE_HOST

DYNAMIC_IMAGES_WEB_ROOT = '/static/CACHE/images/'

DYNAMIC_IMAGES_ROOT = '/usr/local/metaLayer-enterprise/enterprise/metalayercore/imaging/CACHE/'

SENTRY_DSN = 'http://684e9f9df2a94e4187dd0e589ddee586:3c13680ef4fd42edb876cf0da1ff133f@108.166.111.61:9000/3'

TEMPLATE_DIRS = ( '/usr/local/metaLayer-enterprise/enterprise/static/html', )

GOOGLE_ANALYTICS = {
    'account':'UA-34955471-1',
    'site_host':'wwp.metalayer.com',
}

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://localhost:8080/solr',
    'solr_params':SOLR_PARAMS,
    'solr_facets':{}
}

