"""
Django settings for ShevAuthServer project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#o@em3^qw3an5^nijyc-(ik5m#3zlje9)u8^7kxtzjx9h28dr5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE = True


SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'AuthSer',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #'AuthSer.middleware_web.TokenMiddleware',
]


MIDDLEWARE_CLASSES=(
    'AuthSer.middlewareTest.DisableCSRF',
)

ROOT_URLCONF = 'ShevAuthServer.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ShevAuthServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql', # DB명
        'USER' : 'yejin', # 데이터베이스 계정
        'PASSWORD' : 'yejin', # 비밀번호
        'HOST' : '127.0.0.1', # 데이터베이스 주소
        'PORT' : '3306', # 포트번호
    }
}

# Redis 세팅
CACHES = {
    'default' : {
        'BACKEND' : 'redis_cache.RedisCache',
        'LOCATION' : [ # Redis Server의 위치
            'redis://127.0.0.1:6379/1', # Primary Server - Read & Write
        #    '127.0.0.1:6380', # Secondary Server - Read Only
        ],
        #'OPTIONS' : {
        #    'DB' : 1, # Key와 Value가 다른 공간에 존재하는지?
        #    'PASSWORD' : 'yejinredis', # Redis Server 비밀번호
        #   'MASTER_CACHE' : '127.0.0.1:6379',
        #    'PARSER_CLASS' : 'redis.connection.HiredisParser', # C를쓰므로 PythonParser보다 빠름
        #    'SOCKET_TIMEOUT' : 5,
        #    'SOCKET_CONNECT_TIMEOUT' : 5,
        #   'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            #'CONNECTION_POOL_CLASS' : 'redis.BlockingConnectionPool',
            #'CONNECTION_POOL_CLASS_KWARGS' : {
             #   'max_connections' : 50,
             #   'timeout' : 20,

        #    },

    },
    'KEY_PREFIX' : 'example'
}

CACHE_TTL = 60 * 15

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK= {
    'DEFAULT_RENDERER_CLASSES' : (
      'rest_framework.renderers.JSONRenderer',
      'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    #'DEFAULT_PERMISSION_CLASSES' : (
        #'rest_framework.permissions.DjangoModelPermissionsorAnonReadOnly',
        #'rest_framework.permissions.IsAuthenticated,',

    #),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',

    ),
}