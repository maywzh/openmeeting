# encoding: utf-8
from __future__ import absolute_import, unicode_literals
"""
Django settings for meeting project.

Generated by 'django-admin startproject' using Django 1.11.22.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
from kombu import Exchange, Queue

from . import local_settings as ls
from .local_settings import *  # NOQA
from .constance import CONSTANCE_CONFIG  # NOQA
from .celery_annotations import celery_annotations_dict

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: SECRET_KEY is in local_settings

DEBUG = os.environ.get('IS_DEBUG', '1') != '0'

ALLOWED_HOSTS = [
    '*',
]

REDIS_CACHE_URL = 'redis://%s%s@%s:%s/%d' % (':' if ls.REDIS_PASSWORD else '',
                                             ls.REDIS_PASSWORD, ls.REDIS_HOST,
                                             ls.REDIS_PORT, ls.REDIS_CACHE_DB)

# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'constance',
    'import_export',
    'apiview',
    'apps.wechat',
    'apps.meetings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apiview.middlewares.RequestCompatMiddleware',
]

SESSION_ENGINE = "redis_sessions.session"

SESSION_REDIS = {
    'host': ls.REDIS_HOST,
    'port': ls.REDIS_PORT,
    'db': ls.REDIS_SESSION_DB,
    'password': ls.REDIS_PASSWORD,
    'prefix': 'session',
    'socket_timeout': 1
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            '%s:%s' % (ls.REDIS_HOST, ls.REDIS_PORT),
        ],
        'OPTIONS': {
            'DB': ls.REDIS_CACHE_DB,
            'PASSWORD': ls.REDIS_PASSWORD,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1,
        },
    },
}

WSGI_APPLICATION = 'meeting.wsgi.application'

CHANNELS_WS_PROTOCOLS = "apiview"

CHANNEL_LAYERS = {
    "default": {
        "ROUTING": "meeting.routing.channel_routing",
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                'redis://%s%s@%s:%s/%d' %
                (':' if ls.REDIS_PASSWORD else '', ls.REDIS_PASSWORD,
                 ls.REDIS_HOST, ls.REDIS_PORT, ls.REDIS_CHANNEL_DB)
            ]
        }
    },
}

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ls.MYSQL_DBNAME,
        'USER': ls.MYSQL_USERNAME,
        'PASSWORD': ls.MYSQL_PASSWORD,
        'HOST': ls.MYSQL_HOST,
        'PORT': ls.MYSQL_PORT,
        'TEST_CHARSET': "utf8mb4",
        'TEST_COLLATION': "utf8mb4_unicode_ci",
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.wechat.backends.WechatBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

KILL_CSRF = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'

CONSTANCE_REDIS_PREFIX = 'constance:'

CONSTANCE_REDIS_CONNECTION = {
    'host': ls.REDIS_HOST,
    'port': ls.REDIS_PORT,
    'db': ls.REDIS_CONSTANCE_DB,
    'password': ls.REDIS_PASSWORD,
}
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('rest_framework.authentication.SessionAuthentication', ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
        'core.parsers.RawParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'apiview.renderers.JSONPRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny', ),
    'DATETIME_FORMAT':
    DATETIME_FORMAT,
    'TIME_FORMAT':
    TIME_FORMAT,
    'DATE_FORMAT':
    DATE_FORMAT,
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'apiview.renderers.BrowsableAPIRenderer')

GRAPPELLI_ADMIN_TITLE = u'Admin Control Panel'

ROOT_URLCONF = 'meeting.urls'

DEFAULT_FILE_STORAGE = 'core.storages.EnableUrlFileSystemStorage'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format':
            '%(asctime)s %(process)s.%(thread)s %(levelname)s %(module)s.%(funcName)s %(message)s',
            'datefmt': "%y/%m/%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'daphne': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
            'propagate': True
        },
        'django.db': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': [
                'console',
                'mail_admins',
            ],
            'level': 'ERROR',
            'propagate': False,
        },
        'exception': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False
        },
        '': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG',
            'propagate': True
        }
    },
    'root': {
        'handlers': [
            'console',
        ],
        'level': 'DEBUG',
        'propagate': True
    }
}
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
STATIC_ROOT = os.path.join(BASE_DIR, 'www_static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'), )
# celery settings

CELERY_BROKER_URL = 'redis://%s%s@%s:%s/%d' % (
    ':' if ls.REDIS_PASSWORD else '', ls.REDIS_PASSWORD, ls.REDIS_HOST,
    ls.REDIS_PORT, ls.REDIS_CELERY_DB)

CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# 任务执行最长时间20分钟
CELERY_TASK_SOFT_TIME_LIMIT = 1200
CELERY_TASK_TIME_LIMIT = 1200

CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = 'default'

CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']

# 定义执行队列
CELERY_TASK_QUEUES = (Queue('default',
                            Exchange('default'),
                            routing_key='default'),
                      Queue('crontab',
                            Exchange('crontab'),
                            routing_key='crontab'),
                      Queue('async', Exchange('async'), routing_key='async'))

# 制定特定任务路由到特定执行队列
CELERY_TASK_ROUTES = {
    'meeting.celery._async_call': {
        'queue': 'async',
        'routing_key': 'async'
    },
}

CELERY_TASK_ANNOTATIONS = {'*': celery_annotations_dict}

ERROR_CODE_DEFINE = (
    ('ERR_PAGE_SIZE_ERROR', -1001, '页码大小超限'),
    ('ERR_WECHAT_LOGIN', 10001, '需要登录'),
    ('ERR_MEETING_ROOM_TIMEOVER', 20001, '时间已过'),
    ('ERR_MEETING_ROOM_INUSE', 20002, '时间冲突'),
)
