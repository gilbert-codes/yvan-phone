import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Try to read environment variables from a .env file using django-environ.
try:
    import environ
    env = environ.Env(DEBUG=(bool, True))
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        env.read_env(str(env_file))
except Exception:
    env = None

if env:
    SECRET_KEY = env('SECRET_KEY', default='replace-this-with-a-secure-secret')
else:
    SECRET_KEY = 'replace-this-with-a-secure-secret'

if env:
    DEBUG = env.bool('DEBUG', default=True)
else:
    DEBUG = True

if env:
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
else:
    ALLOWED_HOSTS = []

# Optional store location for embedding Google Maps (set via .env or environment variables)
if env:
    STORE_LAT = env('STORE_LAT', default=None)
    STORE_LON = env('STORE_LON', default=None)
    STORE_NAME = env('STORE_NAME', default='Yvan Phone Store')
    GOOGLE_MAPS_API_KEY = env('GOOGLE_MAPS_API_KEY', default=None)
else:
    # fall back to environment variables if django-environ isn't installed
    STORE_LAT = os.environ.get('STORE_LAT')
    STORE_LON = os.environ.get('STORE_LON')
    STORE_NAME = os.environ.get('STORE_NAME', 'Yvan Phone Store')
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yvan_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'yvan_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
