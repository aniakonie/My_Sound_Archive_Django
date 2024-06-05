from website.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'MSA_django_docker',
        'USER': 'postgres',
        'PASSWORD': os.getenv('DB_DOCKER_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432'
    }
}
