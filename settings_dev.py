DEBUG = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@metalayer.com'
EMAIL_HOST_PASSWORD = '##M3taM3ta'
EMAIL_PORT = 587

SITE_HOST = '108.166.98.106'

STATIC_HOST = SITE_HOST

IMAGE_HOST = SITE_HOST

DYNAMIC_IMAGES_WEB_ROOT = '/static/CACHE/images/'

DYNAMIC_IMAGES_ROOT = '/usr/local/metaLayer-enterprise/enterprise/metalayercore/imaging/CACHE/'

SENTRY_DSN = 'http://cb24eedee3b149c0966cb312dedcbd8c:598474230fe84813bfd9d0da84098d2e@108.166.111.61:9000/5'

TEMPLATE_DIRS = ( '/usr/local/metaLayer-enterprise/enterprise/static/html', )
