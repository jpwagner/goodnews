import os

env = os.getenv("ENV")

if env == "production":
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

SECRET_KEY = os.getenv("SECRET_KEY") or '---------------------------------------------------------------'

SCORE_THRESHOLD = 0.1

# HEROKU specific
if env == "production":
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config()
    DATABASES['default']['CONN_MAX_AGE'] = 500
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    DATABASES = os.getenv("DATABASES") or \
    {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
        }
    }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL") or 'redis://localhost:6379/0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
TASTYPIE_DEFAULT_FORMATS = ['json', 'jsonp', 'xml']

BROKER_URL = os.getenv("BROKER_URL") or 'redis://localhost:6379/1'
BROKER_POOL_LIMIT = 8

# site
APPEND_SLASH = True
SITE_ID = 1
SITE_DOMAIN = os.getenv("SITE_DOMAIN") or '127.0.0.1:8000'
if env == "production":
    SITE_DOMAIN = 'www.goodnews123.com'
SITE_NAME = 'GoodNews'
GRAPPELLI_ADMIN_TITLE = SITE_NAME + ' Admin Panel'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_ETAGS = True
USE_TZ = True

# third-party creds
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SOURCES_ENDPOINT = 'https://newsapi.org/v1/sources'
ARTICLES_ENDPOINT = 'https://newsapi.org/v1/articles'

AUTH_USER_MODEL = 'auth.User'
ROOT_URLCONF = 'core.urls'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

STATIC_URL = '/static/'
if env == "production":
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static') # '/var/www/example.com/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'compressor.finders.CompressorFinder'
]

STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.join(PROJECT_ROOT, 'frontend'), 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        }
    },
]

MIDDLEWARE_CLASSES = [
    # if upgrading to django 1.10 look into `MIDDLEWARE` setting

    # 'django.middleware.cache.UpdateCacheMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'tastypie',
    'core',
    'goodnews'
]

WSGI_APPLICATION = 'wsgi.application'

if env == "local":
    from .local import *

