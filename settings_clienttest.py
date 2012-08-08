from settings import SOLR_PARAMS

DEBUG = False

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@metalayer.com'
EMAIL_HOST_PASSWORD = '##M3taM3ta'
EMAIL_PORT = 587

SITE_HOST = 'enterprise.demo.metalayer.com' #'108.166.98.69'

STATIC_HOST = SITE_HOST

IMAGE_HOST = SITE_HOST

DYNAMIC_IMAGES_WEB_ROOT = '/static/CACHE/images/'

DYNAMIC_IMAGES_ROOT = '/usr/local/metaLayer-enterprise/enterprise/metalayercore/imaging/CACHE/'

SENTRY_DSN = 'http://bbd4d07c292840c6a04fbbd534620271:8ca5de91ef1948b2915e1e70eef04b50@108.166.111.61:9000/2'

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

OAUTH2_SETTINGS = {
    'GoogleOauth2Controller':{
        'client_id':'450032264506-i36s4e0mqkjnhmquq0bv2617vh44nu12.apps.googleusercontent.com',
        'client_secret':'8fDtqnPEmhTeUD4th_lLd1RT',
        'redirect_uri':'http://%s/oauth2/google_oauth2_callback' % SITE_HOST
    }
}

