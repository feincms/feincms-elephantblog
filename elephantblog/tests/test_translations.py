# coding: utf-8
import factory
from django.core import management
from django.test.testcases import TestCase
from elephantblog.models import Entry
from feincms.module.extensions import translations
from django.test import Client
from .factories import EntryFactory, create_entries



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


    def testEnvironment(self):
        # Make sure the Entry has a translation extension
        entry = Entry()
        self.assertTrue(hasattr(entry, 'language'))
        self.assertTrue(hasattr(entry, 'translation_of'))
        entries = Entry.objects.order_by('pk')
        entry = entries[0]
        self.assertEqual(entry.pk, 1)
        self.assertEqual(entry.title, u'Entry 1')
        entry = entries[1]
        self.assertEqual(entry.pk, 2)
        self.assertEqual(entry.title, u'Eintrag 1')

