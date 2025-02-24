'''
Boilerplate stuff, import into your own project settings like so:

Conventions:
Using "dproj" as a generic reusable "project" folder instead a unique name every
time (as with the `django-admin startproject` default behavior). "dproj" is also
more grep-able than "project" without false positives. Prefixing all Django-specific
folders with "d" is useful if, e.g., a Flask app is in the same project.
'''
import environ

# to not clash with similar in a specific project
env2 = environ.Env(DEBUG=(bool, False))

DEBUG = env2('DEBUG')

SECRET_KEY = env2('DJANGO_SECRET_KEY')

if DEBUG:
    DATABASES = { 'default': env2.db_url('DJANGO_DB_DEV_URL'), }
    ADMIN_HEADER_BG = '#35b027'  # darker green
else:
    DATABASES = { 'default': env2.db_url('DATABASE_URL'), }
    ADMIN_HEADER_BG = '#c62826'  # darker red

ROOT_URLCONF = 'dproj.urls_root'

WSGI_APPLICATION = 'dproj.wsgi.application'  

# Note that we use Nginx rather than Whitenoise to serve static files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ENV_NAME = env2('DJANGO_ENV_NAME', default='prod')

BASE_APPS = [
    # --------------------------------------------------------------------------
    # startproject apps
    # --------------------------------------------------------------------------
    'django.contrib.admin',
    'djinntoux.dproj.rename.ContribAuth',    # replaces 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # --------------------------------------------------------------------------
    # extra apps
    # --------------------------------------------------------------------------
    'djinntoux.dapp_users',                  # custom user model
    'djinntoux.dproj.rename.ContribSites',   # replaces 'django.contrib.sites',
    'django.contrib.humanize',               # to render integers in templates
    'djangoql',                              # more powerful than DataTables
    'timezone_field',                        # for the custom user model

    # --------------------------------------------------------------------------
    # optional extra apps
    # --------------------------------------------------------------------------
    # 'compressor'
    # 'django_distill',                        # for static site generation
    # 'django_cachekiller',                    # for static site generation
]


# Always use a minimal custom user app for future flexibility.
# OCD note: the database column has a different label than the actual app name
# (for sorting in psql), which must be used here:
AUTH_USER_MODEL = 'zy_users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',                          # added
    'htmlmin.middleware.MarkRequestMiddleware',                         # added
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # extra:
                'djinntoux.dproj.context_reuse.general'
            ],
        },
    },
]


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_TZ = True

TIME_ZONE = 'UTC'