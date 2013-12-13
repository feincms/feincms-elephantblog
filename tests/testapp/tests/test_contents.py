from django.test import TestCase

from .factories import EntryFactory, create_entries


class FeedTestCase(TestCase):
    def test_feed(self):
        entries = create_entries(EntryFactory)
        entries[0].richtextcontent_set.create(
            region='main',
            ordering=1,
            text='Hello world')

        response = self.client.get('/blog/feed/')
        self.assertContains(response, 'rss xmlns:atom')
        self.assertContains(
            response,
            '<title>Blog of the usual elephant</title>',
            1,
        )
        self.assertContains(
            response,
            '<guid>http://testserver/multilang/2012/10/12/eintrag-1/</guid>',
            1,
        )
        self.assertContains(
            response,
            '<guid>http://testserver/multilang/2012/08/12/entry-1/</guid>',
            1,
        )
        self.assertContains(
            response,
            '<description>Hello world</description>',
            1,
        )
