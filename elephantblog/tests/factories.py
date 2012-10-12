# coding: utf-8
from django.template.defaultfilters import slugify
import factory
import datetime
from elephantblog.models import Entry, Category, CategoryTranslation
from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    username='author'
    password='elephant'


class EntryFactory(factory.Factory):
    FACTORY_FOR = Entry
    is_active=True
    is_featured=False

def create_entries(factory):
    author = UserFactory()
    entries = []
    entries.append(factory.create(
        pk=1,
        author=author,
        title=u'Entry 1',
        published_on=datetime.datetime(2012,8,12, 11,0,0),
        last_changed=datetime.datetime(2012,8,12, 15,0,0),
        slug='entry-1'
    ))
    entries.append(factory.create(
        pk=2,
        author=author,
        title=u'Eintrag 1',
        published_on=datetime.datetime(2012,10,12, 11,0,0),
        last_changed=datetime.datetime(2012,10,12, 15,0,0),
        slug='eintrag-1'
    ))
    return entries


class CategoryTranslationFactory(factory.Factory):
    FACTORY_FOR = CategoryTranslation

class CategoryFactory(factory.Factory):
    FACTORY_FOR = Category

def create_category(title):
    category = CategoryFactory.create()
    translation = CategoryTranslationFactory.create(
        parent = category,
        title = title,
        slug = slugify(title)
    )
    return category

