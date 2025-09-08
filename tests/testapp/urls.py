from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from elephantblog.sitemap import EntrySitemap
from elephantblog.urls import elephantblog_patterns


admin.autodiscover()


sitemaps = {
    "elephantblog": EntrySitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("elephantblog.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
    ),
    path(
        "multilang/",
        include(
            elephantblog_patterns(
                list_kwargs={"only_active_language": False},
            )
        ),
    ),
]
