from settings import SOLR_PARAMS

DEBUG = False

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@metalayer.com'
EMAIL_HOST_PASSWORD = '##M3taM3ta'
EMAIL_PORT = 587

SITE_HOST = 'draftfcb.metalayer.com'

STATIC_HOST = SITE_HOST

IMAGE_HOST = SITE_HOST

DYNAMIC_IMAGES_WEB_ROOT = '/static/CACHE/images/'

DYNAMIC_IMAGES_ROOT = '/usr/local/metaLayer-enterprise/enterprise/imaging/CACHE/'

SENTRY_DSN = 'http://417b835ac428418495a82d36ba29d370:8f410e4218184281b09dd13af529c00e@108.166.111.61:9000/7'

TEMPLATE_DIRS = ( '/usr/local/metaLayer-enterprise/enterprise/static/html', )

GOOGLE_ANALYTICS = {
    'account':'UA-31427873-1',
    'site_host':'draftfcb.metalayer.com',
}

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://localhost:8080/solr',
    'solr_params':SOLR_PARAMS,
    'solr_facets':{}
}

