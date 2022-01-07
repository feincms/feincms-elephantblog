from datetime import date

from django.test import TestCase

from .factories import EntryFactory, create_entries


class SitemapTestCase(TestCase):
    def test_sitemap(self):
        entries = create_entries(EntryFactory)
        entries[0].richtextcontent_set.create(
            region="main", ordering=1, text="Hello world"
        )

        response = self.client.get("/sitemap.xml")

        today = date.today().strftime("%Y-%m-%d")

        self.assertContains(
            response,
            f"<lastmod>{today}</lastmod>",
            2,
        )

        self.assertContains(
            response,
            "<loc>http://testserver/multilang/",
            2,
        )
