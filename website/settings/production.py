import os
from dotenv import load_dotenv
import dj_database_url

from website.settings.base import *

load_dotenv()

database_url = os.getenv('DATABASE_URL')
DATABASES['default'] = dj_database_url.parse(database_url)

DEBUG = os.getenv('DEBUG')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 3153600 # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

ALLOWED_HOSTS = [
    'mysoundarchive.com',
    'www.mysoundarchive.com',
    'my-sound-archive-django.onrender.com'
    ]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
