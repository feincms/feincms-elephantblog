# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os


INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "feincms",
    "feincms.module.medialibrary",
    "testapp",
    "elephantblog",
    # 'django_nose',
)

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SECRET_KEY = "elephant"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "runserver.sqlite",
        # 'TEST_NAME': 'blog_test.sqlite',
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

MIDDLEWARE_CLASSES = MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)
SILENCED_SYSTEM_CHECKS = ["1_10.W001"]

ROOT_URLCONF = "testapp.urls"
BLOG_TITLE = "Blog of the usual elephant"
BLOG_DESCRIPTION = ""
TIME_ZONE = "America/Chicago"
USE_TZ = False
DEFAULT_CHARSET = "utf-8"
LANGUAGES = (
    ("en", "English"),
    ("de", "German"),
    ("zh-hans", "Chinese simplified"),
    ("zh-hant", "Chinese traditional"),
)
LANGUAGE_CODE = "en"
USE_I18N = True

DEBUG = True  # tests run with DEBUG=False
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")
MEDIA_URL = "/media/"

MIGRATION_MODULES = {
    # "page": "testapp.migrate.page",
    "medialibrary": "testapp.migrate.medialibrary",
    "elephantblog": "testapp.migrate.elephantblog",
}
