# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string
from django.test.testcases import TestCase

from .factories import EntryFactory, create_entries, create_category


class TemplateTagsTest(TestCase):
    def test_templatetags(self):
        entries = create_entries(EntryFactory)
        category = create_category(title='Category 1')
        create_category(title='Category 2')

        entries[0].categories.add(category)
        entries[1].is_featured = True
        entries[1].save()

        html = render_to_string('test_templatetags.html', {})

        self.assertIn(
            '<p>categories:Category 1,</p>',
            html)
        self.assertIn(
            '<p>categories+empty:Category 1,Category 2,</p>',
            html)
        self.assertIn(
            '<p>months:10.12,08.12,</p>',
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
