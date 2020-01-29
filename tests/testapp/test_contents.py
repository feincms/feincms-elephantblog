from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string
from django.test import TestCase

from elephantblog.contents import BlogEntryListContent, BlogCategoryListContent
from .factories import EntryFactory, create_entries, create_category


class Request(object):
    GET = {"page": 1}


class ContentsTestCase(TestCase):
    def test_contents(self):
        entries = create_entries(EntryFactory)
        entries[0].richtextcontent_set.create(
            region="main", ordering=1, text="Hello world"
        )

        entries[0].is_featured = True
        entries[0].save()
        category = create_category(title="Category 1")
        entries[1].categories.add(category)
        create_category(title="Empty category")

        content = BlogEntryListContent()

        content.process(Request)
        html = render_to_string(*content.render())
        self.assertIn(
            'h2 class="entry-title"><a href="/multilang/2012/10/12/eintrag-1/', html,
        )
        self.assertIn(
            'h2 class="entry-title"><a href="/multilang/2012/08/12/entry-1/"', html,
        )

        content.featured_only = True
        content.process(Request)
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<h2"), 1,
        )

        content.category = category
        content.process(Request)
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<h2"), 0,
        )

        content.featured_only = False
        content.process(Request)
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<h2"), 1,
        )

        content = BlogEntryListContent()
        content.paginate_by = 1
        content.process(Request)
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<h2"), 1,
        )

        Request.GET["page"] = 2
        content.process(Request)
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<h2"), 1,
        )

        Request.GET["page"] = 3
        content.process(Request)
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<h2"), 1,
        )

        Request.GET["page"] = "abc"
        content.process(Request)
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<h2"), 1,
        )

        content = BlogCategoryListContent()
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<li>"), 1,
        )

        content.show_empty_categories = True
        html = render_to_string(*content.render())
        self.assertEqual(
            html.count("<li>"), 2,
        )
