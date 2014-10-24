# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string
from django.test import TransactionTestCase
from django.test.utils import override_settings

from .factories import EntryFactory, create_entries, create_category


class TemplateTagsTest(TransactionTestCase):
    def setUp(self):
        entries = create_entries(EntryFactory)
        category = create_category(title='Category 1')
        create_category(title='Category 2')

        entries[0].categories.add(category)
        entries[1].is_featured = True
        entries[1].save()

    def test_templatetags(self):
        html = render_to_string('test_templatetags.html', {})

        self.assertIn(
            '<p>categories:Category 1,</p>',
            html)
        self.assertIn(
            '<p>categories+empty:Category 1,Category 2,</p>',
            html)
        self.assertIn(
            '<p>months:10.2012,08.2012,</p>',
            html)
        self.assertIn(
            '<p>entries:Eintrag 1,Entry 1,</p>',
            html)
        self.assertIn(
            '<p>entries+featured:Eintrag 1,</p>',
            html)
        self.assertIn(
            '<p>entries+category0:Entry 1,</p>',
            html)
        self.assertIn(
            '<p>entries+category1:</p>',
            html)
        self.assertIn(
            '<p>entries+limit:Eintrag 1,</p>',
            html)


@override_settings(USE_TZ=True, TIME_ZONE='America/Chicago')
class TimezoneTemplateTagsTest(TemplateTagsTest):
    pass
