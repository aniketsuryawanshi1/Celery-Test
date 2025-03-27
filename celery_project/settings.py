import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'channels',  # Add Django Channels
     'django_celery_beat',
     
    'django_celery_results',
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

ROOT_URLCONF = 'celery_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Fixing template path
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

# Use ASGI for WebSockets support
ASGI_APPLICATION = 'celery.asgi.application'


# Database Configuration (Use PostgreSQL)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv("POSTGRES_DB", "default_db"),
#         'USER': os.getenv("POSTGRES_USER", "default_user"),
#         'PASSWORD': os.getenv("POSTGRES_PASSWORD", "default_password"),
#         'HOST': os.getenv("POSTGRES_HOST", "db"),  # 'db' matches Docker Compose service name
#         'PORT': os.getenv("POSTGRES_PORT", "5432"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# Celery Configuration (Fix Redis URLs)

CELERY_BROKER_URL = 'redis://localhost:6379/0'

CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_BEAT_SCHEDULE = {
    "delete-student-objects-every-10-seconds": {
        "task": "core.tasks.delete_student_objects",
        "schedule": 10.0,  # Every 10 seconds
    },
}

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# WebSockets & Channels Configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],  # Use the Redis service from Docker
        },
    },
}




# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / "staticfiles")  # Fixing path
STATICFILES_DIRS = [str(BASE_DIR / "static")]  # Fixing path

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / "media")  # Fixing path

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
