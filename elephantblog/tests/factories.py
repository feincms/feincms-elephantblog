# coding: utf-8
from django.template.defaultfilters import slugify
import factory
import datetime
from elephantblog.models import Entry, Category, CategoryTranslation
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username='author'
    password='elephant'
    email='admin@elephantblog.ch'


class EntryFactory(factory.DjangoModelFactory):
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


def create_chinese_entries(factory):
    entries = create_entries(factory)
    author = entries[0].author
    factory.create(
        pk=3,
        author=author,
        title=u'Entry 2 chinese traditional',
        language='zh-cn',
        translation_of=entries[0],
        published_on=datetime.datetime(2012,10,12, 12,0,0),
        last_changed=datetime.datetime(2012,10,12, 16,0,0),
        slug='entry-2-cn'
    )
    factory.create(
        pk=4,
        author=author,
        title=u'Entry 2 chinese simplified',
        language='zh-tw',
        translation_of=entries[0],
        published_on=datetime.datetime(2012,10,12, 12,0,0),
        last_changed=datetime.datetime(2012,10,12, 16,0,0),
        slug='entry-2-tw'
    )




class CategoryTranslationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CategoryTranslation

class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category

def create_category(title):
    category = CategoryFactory.create()
    translation = CategoryTranslationFactory.create(
        parent = category,
        title = title,
        slug = slugify(title)
    )
    return category

