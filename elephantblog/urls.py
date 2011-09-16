"""
Class-based, modern views for elephantblog
==========================================

Add the following code to ``settings.py`` if you want to integrate Elephantblog
through ApplicationContent::

    def elephantblog_entry_url_app(self):
        from feincms.content.application.models import app_reverse
        return app_reverse('elephantblog_entry_detail', 'elephantblog', kwargs={
            'year': self.published_on.strftime('%Y'),
            'month': self.published_on.strftime('%m'),
            'day': self.published_on.strftime('%d'),
            'slug': self.slug,
            })

    def elephantblog_categorytranslation_url_app(self):
        from feincms.content.application.models import app_reverse
        return app_reverse('elephantblog_category_detail', 'elephantblog', kwargs={
            'slug': self.slug,
            })

    ABSOLUTE_URL_OVERRIDES = {
        'elephantblog.entry': elephantblog_entry_url_app,
        'elephantblog.categorytranslation': elephantblog_categorytranslation_url_app,
    }


NOTE! You need to register the app as follows for the application content snippet::

    Page.create_content_type(ApplicationContent, APPLICATIONS=(
        ('elephantblog', _('Blog'), {'urls': 'elephantblog.urls'}),
        ))

"""

from django.conf.urls.defaults import patterns, include, url

from elephantblog.feeds import EntryFeed
from elephantblog import views


urlpatterns = patterns('',
    url(r'^feed/$', EntryFeed()),
    url(r'^$',
        views.ArchiveIndexView.as_view(),
        name='elephantblog_entry_archive'),
    url(r'^(?P<year>\d{4})/$',
        views.YearArchiveView.as_view(),
        name='elephantblog_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.MonthArchiveView.as_view(),
        name='elephantblog_entry_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.DayArchiveView.as_view(),
        name='elephantblog_entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.DateDetailView.as_view(),
        name='elephantblog_entry_detail'),
    url(r'^category/(?P<slug>[-\w]+)/$',
        views.CategoryArchiveIndexView.as_view(),
        name='elephantblog_category_detail'),
)
