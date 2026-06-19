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

# SECRET KEY
if env:
    SECRET_KEY = env('SECRET_KEY', default='replace-this-with-a-secure-secret')
else:
    SECRET_KEY = 'replace-this-with-a-secure-secret'

# DEBUG - Set to False for production
if env:
    DEBUG = env.bool('DEBUG', default=False)
else:
    DEBUG = False

# ALLOWED HOSTS
if env:
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
else:
    ALLOWED_HOSTS = ['yvan-phone.onrender.com', 'localhost', '127.0.0.1']

# Optional store location for embedding Google Maps
if env:
    STORE_LAT = env('STORE_LAT', default=None)
    STORE_LON = env('STORE_LON', default=None)
    STORE_NAME = env('STORE_NAME', default='Yvan Phone Store')
    GOOGLE_MAPS_API_KEY = env('GOOGLE_MAPS_API_KEY', default=None)
else:
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
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

# ============= STATIC FILES =============
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# WhiteNoise for static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============= MEDIA FILES =============
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============= CLOUDINARY CONFIGURATION =============
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    CLOUD_NAME = "di5r5oiju",
    API_KEY = "347921383578929",
    API_SECRET = "IEm7tgeNxPZig0XD_rxrszfFW7M"
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ============= FIX HTTP/2 & HTTPS ERRORS =============
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

CSRF_TRUSTED_ORIGINS = [
    'https://yvan-phone.onrender.com',
    'http://yvan-phone.onrender.com',
]