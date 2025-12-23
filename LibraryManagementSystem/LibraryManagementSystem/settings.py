"""
Django settings for LibraryManagementSystem project.
Production-ready (PostgreSQL UTC fixed)
"""

import os
from pathlib import Path

# ================================
# BASE DIRECTORY
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# SECURITY
# ================================
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = ["*"]  # change to domain/IP in production

# ================================
# APPLICATIONS
# ================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'LibraryApp',
    'image_uploader_widget',
]

# ================================
# MIDDLEWARE
# ================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryManagementSystem.urls'

# ================================
# TEMPLATES
# ================================
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

WSGI_APPLICATION = 'LibraryManagementSystem.wsgi.application'

# ================================
# DATABASE (POSTGRESQL – UTC FIXED)
# ================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT", "5432"),
        'OPTIONS': {
            'options': '-c timezone=UTC',
        },
    }
}

# ================================
# PASSWORD VALIDATION
# ================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ================================
# INTERNATIONALIZATION (CORRECT)
# ================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # UI timezone
USE_I18N = True
USE_L10N = True
USE_TZ = True               # DB always UTC

# ================================
# STATIC & MEDIA FILES
# ================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ================================
# AUTH SETTINGS
# ================================
AUTH_USER_MODEL = 'LibraryApp.User'
LOGIN_URL = 'lgo'
LOGIN_REDIRECT_URL = 'hm'

# ================================
# EMAIL CONFIG
# ================================
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# ================================
# DEFAULT PRIMARY KEY
# ================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
