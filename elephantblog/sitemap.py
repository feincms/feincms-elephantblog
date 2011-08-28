from django.contrib.sitemaps import Sitemap

from feincms.translations import short_language_code

from models import Entry

class EntrySitemap(Sitemap):
    def items(self):
        return Entry.objects.active().filter(language=short_language_code)

    def lastmod(self, obj):
        return obj.last_changed
