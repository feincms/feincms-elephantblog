from django.conf import settings
from django.conf.urls.defaults import *

from feincms.translations import short_language_code

from elephantblog.feeds import EntryFeed
from elephantblog.models import Entry

"""
The entry dict here is only interpreted during server initialization.
"""
entry_dict = {
    'paginate_by' : 10,
    }

urlpatterns = patterns('elephantblog.views.legacy.views',
    url(r'^feed/$', EntryFeed()),
    url(r'^headlines/$',
        'entry_list',
        dict(entry_dict, template_name='blog/entry_headlines.html'),
        name='elephantblog_headlines'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$',
        'entry',
        name='elephantblog_entry_detail'),
    url(r'^category/(?P<category>[^/]+)/$',
        'entry_list',
        name='elephantblog_category_list'),
    url(r'^(category/(?P<category>[^/]+)/)?((?P<year>\d{4})/)?((?P<month>\d{2})/)?((?P<day>\d{2})/)?$',
        'entry_list',
        entry_dict,
        name='elephantblog_list'),
)

#if 'tagging' in settings.INSTALLED_APPS:
#    urlpatterns += patterns('',url(r'^tag/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list',
#        { 'template_name':'entry_list_tagged.html', 'paginate_by':entry_dict['paginate_by']}, name='elephantblog_tag'),
#)

