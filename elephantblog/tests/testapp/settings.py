import sys
# -*- coding:utf-8 -*-
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'feincms',
    'elephantblog.tests.testapp',
    'elephantblog',
    #'django_nose',
)

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SECRET_KEY = 'elephant'
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'runserver.sqlite',
        #'TEST_NAME': 'blog_test.sqlite',
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
    )

ROOT_URLCONF = 'elephantblog.tests.testapp.urls'
BLOG_TITLE = u'Blog of the usual elephant'
BLOG_DESCRIPTION = ''
TIME_ZONE = 'America/Chicago'
USE_TZ = False
DEFAULT_CHARSET='utf-8'
LANGUAGES = (('en', 'English'), ('de', 'German'),
             ('zh-cn', 'Chinese simplified'), ('zh-tw', 'Chinese traditional'))

DEBUG = True # tests run with DEBUG=False
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

