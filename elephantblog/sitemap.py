from django.contrib.sitemaps import Sitemap

from elephantblog.models import Entry

class EntrySitemap(Sitemap):
    def items(self):
        return Entry.objects.active()

    def lastmod(self, obj):
        return obj.last_changed
