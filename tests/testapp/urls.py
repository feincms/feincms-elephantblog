# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from elephantblog.sitemap import EntrySitemap
from elephantblog.urls import elephantblog_patterns


admin.autodiscover()


sitemaps = {
    'elephantblog': EntrySitemap,
}


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('elephantblog.urls')),
    url(
        r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps},
    ),
)


urlpatterns += patterns(
    '',
    url(
        r'^multilang/',
        include(elephantblog_patterns(
            list_kwargs={'only_active_language': False},
        )),
    ),
)
