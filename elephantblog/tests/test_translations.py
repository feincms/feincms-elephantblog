# coding: utf-8
from django.test.utils import override_settings
import factory
from django.core import management
from django.test.testcases import TestCase
from django.utils import translation

from elephantblog.models import Entry
#from feincms.module.extensions import translations
from django.test import Client
from .factories import EntryFactory, create_entries, create_chinese_entries
from feincms.translations import short_language_code
from .utils import reset_db


class NoTranslationsTest(TestCase):

    def setUp(self):
        create_entries(EntryFactory)

    def testEnvironment(self):
        # Make sure the Entry has no translation attribute
        entry = Entry()
        self.assertFalse(hasattr(entry, 'language'))
        self.assertFalse(hasattr(entry, 'translation_of'))
        entries = Entry.objects.order_by('pk')
        entry = entries[0]
        self.assertEqual(entry.pk, 1)
        self.assertEqual(entry.title, u'Entry 1')
        entry = entries[1]
        self.assertEqual(entry.pk, 2)
        self.assertEqual(entry.title, u'Eintrag 1')

    def testURLs(self):
        c = Client()
        # Test Archive URL
        response = c.get('/blog/')
        self.assertEqual(len(response.context['object_list']), 2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Entry 1')
        self.assertContains(response, u'Eintrag 1')


@override_settings(USE_I18N=True)
class TranslationsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        Entry.register_extensions('feincms.module.extensions.translations',)
        reset_db()
        class EntryFactory(factory.DjangoModelFactory):
            FACTORY_FOR = Entry
            is_active=True
            is_featured=False

        create_chinese_entries(EntryFactory)


    def testTranslation(self):
        # Make sure the Entry has a translation extension
        entry = Entry()
        self.assertTrue(hasattr(entry, 'language'))
        self.assertTrue(hasattr(entry, 'translation_of'))
        # define the language of entry 2
        entries = Entry.objects.order_by('pk')
        entry1 = entries[0]
        self.assertEqual(entry1.pk, 1)
        self.assertEqual(entry1.title, u'Entry 1')
        entry1.language = 'en'
        entry1.save()
        entry2 = entries[1]
        self.assertEqual(entry2.pk, 2)
        self.assertEqual(entry2.title, u'Eintrag 1')
        entry2.language = 'de'
        entry2.translation_of = entry1
        entry2.save()
        entry3 = entries[2]
        entry4 = entries[3]
        self.assertEqual(entry3.language, 'zh-cn')
        self.assertEqual(entry4.language, 'zh-tw')

        entry = Entry.objects.get(language='de')
        self.assertEqual(entry.title, u'Eintrag 1')

        with translation.override('de'):
            c = Client()
            self.assertEqual(short_language_code(), 'de')
            # Test Archive URL
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='de')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, u'Entry 1')
            self.assertContains(response, u'Eintrag 1')
            # test all languages override
            response = c.get('/multilang/', HTTP_ACCEPT_LANGUAGE='de')
            self.assertEqual(len(response.context['object_list']), 4)
            self.assertEqual(response.status_code, 200)


        with translation.override('en'):
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='en')
            self.assertEqual(short_language_code(), 'en')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, u'Entry 1')
            self.assertNotContains(response, u'Eintrag 1')


        with translation.override('zh-cn'):
            self.assertEqual(translation.get_language(), 'zh-cn')
            self.assertEqual(short_language_code(), 'zh')
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='zh-cn')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, u'Entry 2 chinese traditional')
            self.assertNotContains(response, u'Eintrag 1')


        with translation.override('zh-tw'):
            self.assertEqual(translation.get_language(), 'zh-tw')
            self.assertEqual(short_language_code(), 'zh')
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='zh-tw')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, u'Entry 2 chinese simplified')
            self.assertNotContains(response, u'Eintrag 1')





# AttributeError: 'Settings' object has no attribute '_original_allowed_hosts'
# fixed in Django 1.6

# https://github.com/django/django/commit/e2b86571bfa3503fe43adfa92e9c9f4271a7a135