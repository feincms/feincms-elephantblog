# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.contrib import admin

from elephantblog.models import Entry

from .factories import EntryFactory, create_entries
from feincms.extensions import ExtensionModelAdmin

Entry.register_extensions('elephantblog.extensions.blogping',)


@override_settings(SITE_ID=1)
class BlogpingTest(TestCase):

    def setUp(self):
        create_entries(EntryFactory)

    def tearDown(self):
        # TODO: unregister extension
        pass

    def testModel(self):
        # Make sure the Entry has a blogping extension
        entry = Entry()
        self.assertTrue(hasattr(entry, 'pinging'))
        self.assertTrue(hasattr(entry, 'SLEEPING'))
        self.assertTrue(hasattr(entry, 'QUEUED'))
        self.assertTrue(hasattr(entry, 'SENT'))
        self.assertTrue(hasattr(entry, 'UNKNOWN'))

        self.assertEqual(entry.SLEEPING, 10)
        self.assertEqual(entry.pinging, entry.SLEEPING)

    def testSignal(self):
        entry = Entry(author_id=1, language='de', is_active=False)
        self.assertEqual(entry.pinging, entry.SLEEPING)
        entry.save()
        self.assertEqual(entry.pinging, entry.SLEEPING)
        entry.is_active = True
        entry.save()
        self.assertEqual(entry.pinging, entry.QUEUED)

    def testModelAdmin(self):
        modeladmin = ExtensionModelAdmin(Entry, admin.site)
        self.assertEqual(type(modeladmin.model), type(Entry))
