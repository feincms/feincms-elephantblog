"""
Class-based, modern views for elephantblog
==========================================

Use one of those two::

    def elephantblog_entry_url(self):
        from django.core.urlresolvers import reverse
        return reverse('elephantblog_entry_detail', kwargs={
            'year': self.published_on.strftime('%Y'),
            'month': self.published_on.strftime('%m'),
            'day': self.published_on.strftime('%d'),
            'slug': self.slug,
            })

    def elephantblog_entry_url_app(self):
        from feincms.content.application.models import app_reverse
        return app_reverse('elephantblog_entry_detail', 'elephantblog', kwargs={
            'year': self.published_on.strftime('%Y'),
            'month': self.published_on.strftime('%m'),
            'day': self.published_on.strftime('%d'),
            'slug': self.slug,
            })

    ABSOLUTE_URL_OVERRIDES = {
        'elephantblog.Entry': elephantblog_entry_url,
        'elephantblog.Entry': elephantblog_entry_url_app,
    }


NOTE! You need to register the app as follows for the application content snippet::

    Page.create_content_type(ApplicationContent, APPLICATIONS=(
        ('elephantblog', _('Blog'), {'url': 'elephantblog.views.cbv.urls'),
        ))

"""

from django.conf.urls.defaults import patterns, include, url

from elephantblog.feeds import EntryFeed
from elephantblog.models import Entry
from elephantblog.views.cbv import views

try:
    from towel import paginator
except ImportError:
    from django.core import paginator


view_kw = {'queryset': Entry.objects.active()}
paginate_kw = {'paginator_class': paginator.Paginator, 'paginate_by': 10}
date_kw = {'month_format': '%m', 'date_field': 'published_on'}

def combine(*dicts):
    ret = {}
    for d in dicts:
        ret.update(d)
    return ret


urlpatterns = patterns('elephantblog.views.cbv',
    url(r'^feed/$', EntryFeed()),
    url(r'^$', views.ListView.as_view(**combine(view_kw, paginate_kw)), name='elephantblog_entry_list'),
    url(r'^(?P<year>\d{4})/$',
        views.YearArchiveView.as_view(**combine(view_kw, paginate_kw, {
            'date_field': 'published_on', 'make_object_list': True})),
        name='elephantblog_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.MonthArchiveView.as_view(**combine(view_kw, paginate_kw, date_kw)),
        name='elephantblog_entry_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.DayArchiveView.as_view(**combine(view_kw, paginate_kw, date_kw)),
        name='elephantblog_entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.DateDetailView.as_view(**combine(view_kw, date_kw)),
        name='elephantblog_entry_detail'),
)
