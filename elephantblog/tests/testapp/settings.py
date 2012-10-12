# -*- coding:utf-8 -*-
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
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
        'NAME': 'testapp.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',        
    }
}

ROOT_URLCONF = 'elephantblog.tests.testapp.urls'
BLOG_TITLE = u'Blog of the usual elephant'
BLOG_DESCRIPTION = ''
TIME_ZONE = 'America/Chicago'
USE_TZ = False
LANGUAGES = (('en', 'English'), ('de', 'German'),)