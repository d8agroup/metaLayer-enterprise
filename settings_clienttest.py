from settings import SOLR_PARAMS

DEBUG = False

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@metalayer.com'
EMAIL_HOST_PASSWORD = '##M3taM3ta'
EMAIL_PORT = 587

SITE_HOST = '108.166.98.69'

STATIC_HOST = SITE_HOST

IMAGE_HOST = SITE_HOST

DYNAMIC_IMAGES_WEB_ROOT = '/static/CACHE/images/'

DYNAMIC_IMAGES_ROOT = '/usr/local/metaLayer-enterprise/enterprise/imaging/CACHE/'

SENTRY_DSN = 'http://a9d2974e46d3488f8c6afd26771e3da5:4e97f687aa914069b6a0068ad4250939@108.166.111.61:9000/6'

TEMPLATE_DIRS = ( '/usr/local/metaLayer-enterprise/enterprise/static/html', )

GOOGLE_ANALYTICS = {
    'account':'UA-30142874-1',
    'site_host':'metalayer.com',
}

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://108.166.59.173:8080/solr',
    'solr_params':SOLR_PARAMS,
    'solr_facets':{}
}

