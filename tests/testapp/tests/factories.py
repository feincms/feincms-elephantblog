# coding: utf-8

from __future__ import absolute_import, unicode_literals

import datetime
import pytz
import factory

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings


from elephantblog.models import Entry, Category, CategoryTranslation


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = 'author'
    password = 'elephant'
    email = 'admin@elephantblog.ch'


class EntryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Entry

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
        language='zh-hans',
        translation_of=entries[0],
        published_on=datetime.datetime(2012, 10, 12, 12, 0, 0),
        last_changed=datetime.datetime(2012, 10, 12, 16, 0, 0),
        slug='entry-2-cn'
    )
    factory.create(
        pk=4,
        author=author,
        title='Entry 2 chinese simplified',
        language='zh-hant',
        translation_of=entries[0],
        published_on=datetime.datetime(2012, 10, 12, 12, 0, 0),
        last_changed=datetime.datetime(2012, 10, 12, 16, 0, 0),
        slug='entry-2-tw'
    )


class CategoryTranslationFactory(factory.DjangoModelFactory):
    class Meta:
        model = CategoryTranslation


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category


def create_category(title):
    category = CategoryFactory.create()
    CategoryTranslationFactory.create(
        parent=category,
        title=title,
        slug=slugify(title)
    )
    return category
