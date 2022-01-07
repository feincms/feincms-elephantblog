import datetime
import zoneinfo

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from elephantblog.models import Entry


class TimezoneTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username="author", password="elephant")

    def test_chicago_night(self):
        chicago_tz = zoneinfo.ZoneInfo("America/Chicago")
        published_date = datetime.datetime(
            year=2012, month=3, day=3, hour=1, minute=30, tzinfo=chicago_tz
        )
        entry = Entry.objects.create(
            is_active=True,
            author=self.author,
            slug="test-entry",
            published_on=published_date,
        )

        # print entry
        # print entry.get_absolute_url()
        self.assertEqual(entry.published_on, published_date)
        response = self.client.get(entry.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_chicago_evening(self):
        chicago_tz = zoneinfo.ZoneInfo("America/Chicago")
        published_date = datetime.datetime(
            year=2012, month=3, day=3, hour=22, minute=30, tzinfo=chicago_tz
        )

        entry = Entry.objects.create(
            is_active=True,
            author=self.author,
            slug="test-entry",
            published_on=published_date,
        )

        # print entry.published_on
        # print entry.get_absolute_url()
        self.assertEqual(entry.published_on, published_date)
        response = self.client.get(entry.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_moscow_night(self):
        moscow_tz = zoneinfo.ZoneInfo("Europe/Moscow")
        published_date = datetime.datetime(
            year=2012, month=3, day=3, hour=1, minute=30, tzinfo=moscow_tz
        )
        entry = Entry.objects.create(
            is_active=True,
            author=self.author,
            slug="test-entry",
            published_on=published_date,
        )

        response = self.client.get(entry.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_permalink_equality(self):
        urls = []
        for tzinfo in (
            zoneinfo.ZoneInfo("America/Chicago"),
            zoneinfo.ZoneInfo("Europe/Moscow"),
        ):
            published_date = datetime.datetime(
                year=2012, month=3, day=3, hour=1, minute=30, tzinfo=tzinfo
            )

            entry = Entry.objects.create(
                is_active=True,
                author=self.author,
                slug="test-entry",
                published_on=published_date,
            )

            urls.append(entry.get_absolute_url())
            entry.delete()

        url_chicago, url_moscow = urls
        self.assertNotEqual(url_chicago, url_moscow)
        urls = []
        for tzinfo, day, hour in [
            (zoneinfo.ZoneInfo("America/Chicago"), 2, 15),
            (zoneinfo.ZoneInfo("Europe/Moscow"), 3, 1),
        ]:
            published_date = datetime.datetime(
                year=2012, month=3, day=day, hour=hour, minute=30, tzinfo=tzinfo
            )

            entry = Entry.objects.create(
                is_active=True,
                author=self.author,
                slug="test-entry",
                published_on=published_date,
            )
            urls.append(entry.get_absolute_url())
            entry.delete()

        url_chicago, url_moscow = urls
        self.assertEqual(url_chicago, url_moscow)
