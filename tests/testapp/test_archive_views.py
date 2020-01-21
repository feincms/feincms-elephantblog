# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.test import Client

import six

from feincms.module.medialibrary.models import MediaFile

from elephantblog.models import Entry
from elephantblog import views as blogviews

from .factories import EntryFactory, create_entries, create_category


@override_settings(SITE_ID=1)
class GenericViewsTest(TestCase):
    def setUp(self):
        create_entries(EntryFactory)

    def testURLs(self):
        c = Client()
        # Test Archive URL
        response = c.get("/blog/")
        self.assertTrue(
            isinstance(response.context["view"], blogviews.ArchiveIndexView)
        )
        self.assertEqual(len(response.context["object_list"]), 2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entry 1")
        self.assertContains(response, "Eintrag 1")

        # Test year archive
        response = c.get("/blog/2012/")
        self.assertTrue(isinstance(response.context["view"], blogviews.YearArchiveView))
        self.assertEqual(len(response.context["object_list"]), 2)
        self.assertEqual(
            response.context["view"].get_template_names(),
            ["elephantblog/entry_archive.html"],
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "News for 2012")
        self.assertContains(response, "Entry 1")
        self.assertContains(response, "Eintrag 1")
        # No entries in 2011:
        response = c.get("/blog/2011/")
        self.assertEqual(response.status_code, 404)

        # Test month archive
        response = c.get("/blog/2012/10/")
        self.assertTrue(
            isinstance(response.context["view"], blogviews.MonthArchiveView)
        )
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertEqual(response.status_code, 200)
        six.assertRegex(
            self, response.content.decode("utf-8"), r"News\s+for October 2012"
        )
        self.assertContains(response, "Eintrag 1")
        response = c.get("/blog/2012/08/")
        self.assertEqual(len(response.context["object_list"]), 1)
        six.assertRegex(
            self, response.content.decode("utf-8"), r"News\s+for August 2012"
        )
        self.assertContains(response, "Entry 1")
        response = c.get("/blog/2012/06/")
        self.assertEqual(response.status_code, 404)

        # Test day archive
        response = c.get("/blog/2012/10/12/")
        self.assertTrue(isinstance(response.context["view"], blogviews.DayArchiveView))
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertEqual(response.status_code, 200)
        six.assertRegex(
            self, response.content.decode("utf-8"), r"News\s+for Oct. 12, 2012"
        )
        self.assertContains(response, "Eintrag 1")
        response = c.get("/blog/2012/08/12/")
        self.assertEqual(len(response.context["object_list"]), 1)
        six.assertRegex(
            self, response.content.decode("utf-8"), r"News\s+for Aug. 12, 2012"
        )
        self.assertContains(response, "Entry 1")
        # No entries in 2011:
        response = c.get("/blog/2012/10/13/")
        self.assertEqual(response.status_code, 404)

        # Test category archive
        # assign a category to the entry
        category1 = create_category("Category 1")
        category2 = create_category("Category 2")
        entry = Entry.objects.get(slug="entry-1")
        entry.categories.add(category1)
        entry.categories.add(category2)
        entry = Entry.objects.get(slug="eintrag-1")
        entry.categories.add(category2)

        response = c.get("/blog/category/category-1/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            isinstance(response.context["view"], blogviews.CategoryArchiveIndexView)
        )
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertContains(response, "Entry 1")
        self.assertNotContains(response, "Eintrag 1")

        response = c.get("/blog/category/category-2/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            isinstance(response.context["view"], blogviews.CategoryArchiveIndexView)
        )
        self.assertEqual(len(response.context["object_list"]), 2)
        self.assertContains(response, "Entry 1")
        self.assertContains(response, "Eintrag 1")

    def test_lookup_related(self):
        entry = Entry.objects.get(slug="entry-1")
        richtext = entry.richtextcontent_set.create(
            ordering=1, region="main", text="<b>Hello</b>"
        )

        image = entry.mediafilecontent_set.create(
            ordering=2,
            region="main",
            mediafile=MediaFile.objects.create(type="image", file="test.jpg",),
        )

        c = Client()

        response = c.get("/blog/2012/08/12/entry-1/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context["view"], blogviews.DateDetailView))
        self.assertContains(response, "Entry 1")
        self.assertContains(response, "<b>Hello</b>")
        self.assertContains(response, 'src="/media/test.jpg"')

        self.assertEqual(response.context["entry"].first_image, image)
        self.assertEqual(response.context["entry"].first_richtext, richtext)

        response = c.get("/blog/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object_list"][1].first_image, image)
        self.assertEqual(response.context["object_list"][1].first_richtext, richtext)
