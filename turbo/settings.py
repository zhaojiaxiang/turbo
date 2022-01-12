"""
Django settings for turbo project.

Generated by 'django-admin startproject' using Django 2.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import os
import sys

from django.utils.translation import ugettext_lazy as _
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .config file
environ.Env.read_env(str(BASE_DIR) + "/.config")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kh1)88er$5mnde9=mc2vtg6$n5*b(shj@&2o49p-72a&ku73_!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', True)

ALLOWED_HOSTS = ['*']

# Django Applications
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third Party Applications
THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters'
]

# Local Applications
LOCAL_APPS = [
    'accounts',
    'rbac',
    'liaisons',
    'checkouts',
    'projects',
    'qa',
    'reports',
    'reviews',
    'systems',
    'dashboard'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'utils.middleware.logger.handler.LoggerMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.logger.handler.CollectionMiddleware',
]

ROOT_URLCONF = 'turbo.urls'

AUTH_USER_MODEL = 'accounts.User'

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

WSGI_APPLICATION = 'turbo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DEFAULT_NAME'),
        'USER': env('DEFAULT_USER'),
        'PASSWORD': env('DEFAULT_PASSWORD'),
        'HOST': env('DEFAULT_HOST'),
        'PORT': env('DEFAULT_PORT'),
        'ATOMIC_REQUESTS': True,
        # 设置数据库持久化连接
        'CONN_MAX_AGE': env.int('CONN_MAX_AGE', default=60)
    },
    'ManPower': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': env('MANPOWER_NAME'),
        'USER': env('MANPOWER_USER'),
        'PASSWORD': env('MANPOWER_PASSWORD'),
        'HOST': env('MANPOWER_HOST'),
        'PORT': env('MANPOWER_PORT'),
        'CONN_MAX_AGE': env.int('CONN_MAX_AGE', default=60)
    }
}

# 自定义全局变量
# 该状态为False时，联络票更新不参与SLIMS数据同步
SLIMS_STATUS = env.bool('SLIMS_STATUS', False)
# 使用Django自带邮件发送服务，配置项
EMAIL_HOST = env('MAIL_HOST')
EMAIL_HOST_USER = env('MAIL_USER')
EMAIL_HOST_PASSWORD = env('MAIL_KEY')
EMAIL_PORT = env('MAIL_PORT')

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# django 多语言支持配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 用于生成替换的多语言的文件夹
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('en', _('English')),
    ('zh-Hans', _('中文')),
)

# python manage.py makemessages -l zh_hans --ignore=venv/*
# django-admin compilemessages

# 前端富文本编辑器展示图片时需要使用sendfile，使用sendfile必须配置SENDFILE_BACKEND
SENDFILE_BACKEND = "sendfile.backends.development"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOG_PATH = os.path.join(BASE_DIR, "logs")

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Simple JWT Token
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # 重新指定schema_class的配置, 否则访问 /docs/时报错
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'EXCEPTION_HANDLER': 'utils.exception.handler.api_exception_handler'
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=env.int("ACCESS_TOKEN_LIFETIME")),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(minutes=env.int("REFRESH_TOKEN_LIFETIME")),
    'ROTATE_REFRESH_TOKENS': True,
}

#
# sentry_sdk.init(
#     dsn="http://a0455dc257fa4673b9a866f93ab3aaed@192.168.85.128:9000/4",
#     integrations=[DjangoIntegration()],
#
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,
#
#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )