DEBUG = True

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://50.57.164.216:8080/solr',
    'solr_params':'wt=json&facet=on&sort=time+desc&rows=100&facet.mincount=1',
    'solr_facets':{
        'source_display_name':{
            'display_name':'Source',
            'enabled':True,
            },
        'channel_type':{
            'display_name':'Type',
            'enabled':True,
            },
        'tags':{
            'display_name':'Tags',
            'enabled':True,
            }
    }
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

DYNAMIC_IMAGES_ROOT = '/home/matt/code/metaLayer/enterprise/imaging/CACHE/'

SENTRY_DSN = 'http://cb24eedee3b149c0966cb312dedcbd8c:598474230fe84813bfd9d0da84098d2e@108.166.111.61:9000/5'

TEMPLATE_DIRS = ( '/home/matt/code/metaLayer/enterprise/static/html', )

STATICFILES_DIRS = ( '/home/matt/code/metaLayer/enterprise/static/', )

STATICFILES_FINDERS = ( 'django.contrib.staticfiles.finders.FileSystemFinder', )

