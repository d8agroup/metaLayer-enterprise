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

OAUTH2_SETTINGS = {
    'GoogleOauth2Controller':{
        'client_id':'450032264506-i36s4e0mqkjnhmquq0bv2617vh44nu12.apps.googleusercontent.com',
        'client_secret':'8fDtqnPEmhTeUD4th_lLd1RT',
        'redirect_uri':'http://%s/oauth2/google_oauth2_callback' % SITE_HOST
    },
    'FacebookOauth2Controller': {
        'client_id': '457768257589473',
        'client_secret': 'd93ba13ce81f2f578f345865aaea2269',
        'redirect_uri':'http://%s/oauth2/facebook_oauth2_callback' % SITE_HOST
    }
}