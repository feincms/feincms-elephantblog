# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from elephantblog.urls import elephantblog_patterns


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('elephantblog.urls'))
)


urlpatterns += patterns(
    '',
    url(r'^multilang/', include(elephantblog_patterns(
        list_kwargs={'only_active_language': False},
        ))),
)
