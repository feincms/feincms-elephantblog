# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'feincms',
    'testapp',
    'elephantblog',
    # 'django_nose',
)

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SECRET_KEY = 'elephant'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'runserver.sqlite',
        # 'TEST_NAME': 'blog_test.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'testapp.urls'
BLOG_TITLE = 'Blog of the usual elephant'
BLOG_DESCRIPTION = ''
TIME_ZONE = 'America/Chicago'
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
    ('zh-cn', 'Chinese simplified'),
    ('zh-tw', 'Chinese traditional'),
)
LANGUAGE_CODE = 'en'
USE_I18N = True

DEBUG = True  # tests run with DEBUG=False
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    # request context processor is needed
    'django.core.context_processors.request',
)
STATIC_URL = '/static/'
