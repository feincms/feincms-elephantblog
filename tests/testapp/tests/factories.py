# coding: utf-8

from __future__ import absolute_import, unicode_literals

import datetime
import pytz

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.dateparse import parse_datetime
from django.conf import settings

import factory

from elephantblog.models import Entry, Category, CategoryTranslation


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = 'author'
    password = 'elephant'
    email = 'admin@elephantblog.ch'


class EntryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Entry
    is_active = True
    is_featured = False


def create_entries(factory):
    author = UserFactory()
    entries = []
    date1 = datetime.datetime(2012, 8, 12, 11, 0, 0)
    delta = datetime.timedelta(hours=4)
    date2 = datetime.datetime(2012, 10, 12, 11, 1, 0)
    if settings.USE_TZ:
        date1 = pytz.timezone(settings.TIME_ZONE).localize(date1, is_dst=None)
        date2 = pytz.timezone(settings.TIME_ZONE).localize(date2, is_dst=None)

    entries.append(factory.create(
        pk=1,
        author=author,
        title='Entry 1',
        published_on=date1,
        last_changed=date1+delta,
        slug='entry-1',
        language='en',
    ))
    entries.append(factory.create(
        pk=2,
        author=author,
        title='Eintrag 1',
        published_on=date2,
        last_changed=date2+delta,
        slug='eintrag-1',
        language='en',
    ))
    return entries


def create_chinese_entries(factory):
    entries = create_entries(factory)
    author = entries[0].author
    factory.create(
        pk=3,
        author=author,
        title='Entry 2 chinese traditional',
        language='zh-cn',
        translation_of=entries[0],
        published_on=datetime.datetime(2012, 10, 12, 12, 0, 0),
        last_changed=datetime.datetime(2012, 10, 12, 16, 0, 0),
        slug='entry-2-cn'
    )
    factory.create(
        pk=4,
        author=author,
        title='Entry 2 chinese simplified',
        language='zh-tw',
        translation_of=entries[0],
        published_on=datetime.datetime(2012, 10, 12, 12, 0, 0),
        last_changed=datetime.datetime(2012, 10, 12, 16, 0, 0),
        slug='entry-2-tw'
    )


class CategoryTranslationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CategoryTranslation


class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category


def create_category(title):
    category = CategoryFactory.create()
    CategoryTranslationFactory.create(
        parent=category,
        title=title,
        slug=slugify(title)
    )
    return category
