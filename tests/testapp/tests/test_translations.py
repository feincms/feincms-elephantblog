# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.test import Client
from django.test.testcases import TestCase
from django.utils import translation

from feincms.translations import short_language_code

from elephantblog.models import Entry
from .factories import EntryFactory, create_chinese_entries


class TranslationsTest(TestCase):
    def testTranslation(self):
        create_chinese_entries(EntryFactory)

        # Make sure the Entry has a translation extension
        entry = Entry()
        self.assertTrue(hasattr(entry, 'language'))
        self.assertTrue(hasattr(entry, 'translation_of'))

        # define the language of entry 2
        entries = Entry.objects.order_by('pk')
        entry1 = entries[0]
        self.assertEqual(entry1.pk, 1)
        self.assertEqual(entry1.title, 'Entry 1')
        entry1.language = 'en'
        entry1.save()
        entry2 = entries[1]
        self.assertEqual(entry2.pk, 2)
        self.assertEqual(entry2.title, 'Eintrag 1')
        entry2.language = 'de'
        entry2.translation_of = entry1
        entry2.save()
        entry3 = entries[2]
        entry4 = entries[3]
        self.assertEqual(entry3.language, 'zh-cn')
        self.assertEqual(entry4.language, 'zh-tw')

        entry = Entry.objects.get(language='de')
        self.assertEqual(entry.title, 'Eintrag 1')

        with translation.override('de'):
            c = Client()
            self.assertEqual(short_language_code(), 'de')
            # Test Archive URL
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='de')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, 'Entry 1')
            self.assertContains(response, 'Eintrag 1')
            # test all languages override
            response = c.get('/multilang/', HTTP_ACCEPT_LANGUAGE='de')
            self.assertEqual(len(response.context['object_list']), 4)
            self.assertEqual(response.status_code, 200)

        with translation.override('en'):
            c = Client()
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='en')
            self.assertEqual(short_language_code(), 'en')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Entry 1')
            self.assertNotContains(response, 'Eintrag 1')

        with translation.override('zh-cn'):
            c = Client()
            self.assertEqual(translation.get_language(), 'zh-cn')
            self.assertEqual(short_language_code(), 'zh')
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='zh-cn')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Entry 2 chinese traditional')
            self.assertNotContains(response, 'Eintrag 1')

        with translation.override('zh-tw'):
            c = Client()
            self.assertEqual(translation.get_language(), 'zh-tw')
            self.assertEqual(short_language_code(), 'zh')
            response = c.get('/blog/', HTTP_ACCEPT_LANGUAGE='zh-tw')
            self.assertEqual(len(response.context['object_list']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Entry 2 chinese simplified')
            self.assertNotContains(response, 'Eintrag 1')
