# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from elephantblog.sitemap import EntrySitemap
from elephantblog.urls import elephantblog_patterns


admin.autodiscover()


sitemaps = {
    'elephantblog': EntrySitemap,
}


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('elephantblog.urls')),
    url(
        r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
    ),
    url(
        r'^multilang/',
        include(elephantblog_patterns(
            list_kwargs={'only_active_language': False},
        )),
    ),
]
