# -*- coding:utf-8 -*-
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'feincms',
    'elephantblog.tests.testapp',
    'elephantblog',
)

SECRET_KEY = 'elephant'
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
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
