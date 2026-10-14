from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'solo-desarrollo-local-tareas-no-produccion')
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
INSTALLED_APPS = ['tareas']
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {},
}]
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Guatemala'
USE_TZ = True
