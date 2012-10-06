.. _installation:

=========================
Installation instructions
=========================


Requirements
============

ElephantBlog needs at least:

* Django v1.3 (get it here: https://github.com/django/django)
* FeinCMS v1.5 (get it here: https://github.com/feincms/feincms)
* TinyMCE_ or any other Richtext editor. TinyMCE goes in /media/js/tiny_mce.

.. _TinyMCE: http://www.tinymce.com/download/download.php

Optional packages:

* Pinging_ for search engine pinging.

.. _Pinging: https://github.com/matthiask/pinging

Installation
============

You can install elephantblog using ``pip install feincms-elephantblog``.

* Add ``elephantblog`` to your ``INSTALLED_APPS`` in your ``settings.py``

In your ``application/models.py`` register the blog module, extensions and content types::

    from feincms.content.richtext.models import RichTextContent
    from feincms.content.medialibrary.v2 import MediaFileContent
    import feincms_cleanse

    from elephantblog.models import Entry

    Entry.register_extensions('feincms.module.extensions.datepublisher',
                              'feincms.module.extensions.translations',
                              'elephantblog.extensions.blogping',
    )
    Entry.register_regions(
        ('main', _('Main content area')),
    )
    Entry.create_content_type(RichTextContent,
                        cleanse=feincms_cleanse.cleanse_html, regions=('main',))
    Entry.create_content_type(MediaFileContent, TYPE_CHOICES=(
        ('default', _('default')),
    ))


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
Just make sure you have registered the ``navigation`` extension on your Page object.
You have to import the correct module depending on the mptt tags you are using
to build your navigation. Available are ``treeinfo`` and ``recursetree``.

Add those lines to the ``models.py`` of your app::

    from elephantblog.navigation_extensions import treeinfo  # so the extensions can be found.

    Page.register_extensions('navigation',)


Settings
--------

You can set the number of entries per page with the following setting::

    BLOG_PAGINATE_BY = 10