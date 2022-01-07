"""
Class-based, modern views for elephantblog
==========================================

Add the following code to ``settings.py`` if you want to integrate Elephantblog
through ApplicationContent::

    def elephantblog_entry_url_app(self):
        from feincms.apps import app_reverse
        return app_reverse(
            'elephantblog_entry_detail',
            'elephantblog',
            kwargs={
                'year': self.published_on.strftime('%Y'),
                'month': self.published_on.strftime('%m'),
                'day': self.published_on.strftime('%d'),
                'slug': self.slug,
            })

    def elephantblog_categorytranslation_url_app(self):
        from feincms.apps import app_reverse
        return app_reverse(
            'elephantblog_category_detail',
            'elephantblog',
            kwargs={
                'slug': self.slug,
            })

    ABSOLUTE_URL_OVERRIDES = {
        'elephantblog.entry': elephantblog_entry_url_app,
        'elephantblog.categorytranslation':\
            elephantblog_categorytranslation_url_app,
    }


NOTE! You need to register the app as follows for the application content
snippet::

    Page.create_content_type(ApplicationContent, APPLICATIONS=(
        ('elephantblog', _('Blog'), {'urls': 'elephantblog.urls'}),
        ))

"""


from django.urls import path, re_path

from elephantblog import views
from elephantblog.feeds import EntryFeed


def elephantblog_patterns(list_kwargs={}, detail_kwargs={}):
    """
    Returns an instance of ready-to-use URL patterns for the blog.

    In the future, we will have a few configuration parameters here:

    - A parameter to specify a custom mixin for all view classes (or for
      list / detail view classes?)
    - Parameters to specify the language handling (probably some initialization
      arguments for the ``as_view`` methods)
    - The format of the month (three chars or two digits)
    - etc.
    """
    return [
        path("feed/", EntryFeed(), name="elephantblog_feed"),
        path(
            "",
            views.ArchiveIndexView.as_view(**list_kwargs),
            name="elephantblog_entry_archive",
        ),
        re_path(
            r"^(?P<year>\d{4})/$",
            views.YearArchiveView.as_view(**list_kwargs),
            name="elephantblog_entry_archive_year",
        ),
        re_path(
            r"^(?P<year>\d{4})/(?P<month>\d{2})/$",
            views.MonthArchiveView.as_view(**list_kwargs),
            name="elephantblog_entry_archive_month",
        ),
        re_path(
            r"^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$",
            views.DayArchiveView.as_view(**list_kwargs),
            name="elephantblog_entry_archive_day",
        ),
        re_path(
            r"^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/" r"(?P<slug>[-\w]+)/$",
            views.DateDetailView.as_view(**detail_kwargs),
            name="elephantblog_entry_detail",
        ),
        re_path(
            r"^category/(?P<slug>[-\w]+)/$",
            views.CategoryArchiveIndexView.as_view(**list_kwargs),
            name="elephantblog_category_detail",
        ),
        re_path(
            r"^author/(?P<pk>[-\w]+)/$",
            views.AuthorArchiveIndexView.as_view(**list_kwargs),
            name="elephantblog_author_detail",
        ),
    ]


# Backwards compatibility: Create a URL patterns object with the default
# configuration
urlpatterns = elephantblog_patterns()
