from django.contrib.sitemaps import Sitemap

from feincms.translations import short_language_code

from elephantblog.models import Entry

class EntrySitemap(Sitemap):
    def items(self):
        return Entry.objects.active()

    def lastmod(self, obj):
        return obj.last_changed
