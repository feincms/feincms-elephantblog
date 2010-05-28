from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _

from feincms.translations import short_language_code

from models import Entry

class EntryFeed(Feed):
    title = _('title undefined')
    link = '/blog/'
    description = _('description undefined')
    
    def items(self):
        return Entry.objects.active().filter(language=short_language_code).order_by('-published_on')

    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        content = u''.join(c.render() for c in item.content.main)
        return content