# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

from elephantblog.urls import elephantblog_patterns


urlpatterns = patterns('',
    url('^blog/', include('elephantblog.urls'))
)


urlpatterns += patterns('',
    url(r'^multilang/', include(elephantblog_patterns(
        list_kwargs={'only_active_language': False},
        ))),
)
