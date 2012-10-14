# coding: utf-8
from django.test.utils import override_settings
import factory
from django.core import management
from django.test.testcases import TestCase
from django.utils import translation
from elephantblog.models import Entry
from feincms.module.extensions import translations
from django.test import Client
from .factories import EntryFactory, create_entries
from feincms.translations import short_language_code


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
        Entry.register_extension(translations.register)
        management.call_command('reset', 'elephantblog', interactive=False)
        class EntryFactory(factory.Factory):
            FACTORY_FOR = Entry
            is_active=True
            is_featured=False

        create_entries(EntryFactory)


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

        with translation.override('en'):
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='en')
            self.assertEqual(short_language_code(), 'en')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, u'Entry 1')
            self.assertNotContains(response, u'Eintrag 1')



