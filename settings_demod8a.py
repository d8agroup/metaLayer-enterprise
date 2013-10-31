from settings import SOLR_PARAMS

DEBUG = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@metalayer.com'
EMAIL_HOST_PASSWORD = '##M3taM3ta'
EMAIL_PORT = 587

SITE_HOST = 'alpha.upstream-analytics.com' #'162.209.90.27'

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

#OAUTH Settings for Google and Facebook
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

# Configure Twython
TWYTHON_CONFIG = {
    'app_key': '4ZmCib5T4O0hJ2JFlmwQ',
    'app_secret': '6787BrC0h4KsUSNkujeaZbCoyFsBpBDTlHfmmk4lJdc',
    'oauth_token': '8208232-hw7cbLuXaWNb3MfGkjlJF9YI73eihcIcVrC9Kukseb',
    'oauth_secret': 'SuYb7LZtB50pthj5SlJRhOJr20Lk0b4489NQnSPtTwCs2'
}
