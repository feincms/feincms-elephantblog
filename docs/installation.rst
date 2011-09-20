.. _installation:

=========================
Installation instructions
=========================


Requirements
============

ElephantBlog needs at least:

* Django v1.3 (get it here: https://github.com/django/django)
* FeinCMS v1.5 (get it here: https://github.com/feincms/feincms, ``next`` branch)


Installation
============

At this time, there is no prebundled installation file to install via pip or easy_install. So get
the source at: https://github.com/feincms/feincms-elephantblog/

* Make sure to add the ``elephantblog`` to your Python path.
* Add ``elephantblog`` to your ``INSTALLED_APPS`` in your ``settings.py``

In your ``application/models.py`` register the blog module and content types::

    from feincms.content.richtext.models import RichTextContent

    from elephantblog.models import Entry

    Entry.register_regions(
        ('main', _('Main content area')),
    )
    Entry.create_content_type(RichTextContent, cleanse=False, regions=('main',))


.. note::

    Of course, you can create all of the content types that you have for your FeinCMS Page.


Integrating Standalone:
-----------------------

Add the following lines to your urls.py::

    # Elephantblog urls
    urlpatterns += patterns('',
        url(r'^blog/', include('elephantblog.urls')),
    )


FeinCMS Integration as ApplicationContent
-----------------------------------------

You can easily add the blog to your FeinCMS Page based app.

Just import and add the ApplicationContent to your Page object::

    from feincms.content.application.models import ApplicationContent

    # init your Page object here

    Page.create_content_type(ApplicationContent, APPLICATIONS=(
            ('elephantblog.urls', 'Blog'),
    ))

Use Django's ``ABSOLUTE_URL_OVERRIDES`` mechanism to override the
``get_absolute_url`` method of blog entries and categories. Add the
following methods and settings to your ``settings.py`` file::

    def elephantblog_entry_url_app(self):
        from feincms.content.application.models import app_reverse
        return app_reverse('elephantblog_entry_detail', 'elephantblog.urls', kwargs={
            'year': self.published_on.strftime('%Y'),
            'month': self.published_on.strftime('%m'),
            'day': self.published_on.strftime('%d'),
            'slug': self.slug,
            })

    def elephantblog_categorytranslation_url_app(self):
        from feincms.content.application.models import app_reverse
        return app_reverse('elephantblog_category_detail', 'elephantblog.urls', kwargs={
            'slug': self.slug,
            })

    ABSOLUTE_URL_OVERRIDES = {
        'elephantblog.entry': elephantblog_entry_url_app,
        'elephantblog.categorytranslation': elephantblog_categorytranslation_url_app,
    }


Elephantblog also provides a navigation extension for FeinCMS.
Just make sure you have registered the 'navigation' extension on your Page object.
