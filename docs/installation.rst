.. _installation:

=========================
Installation instructions
=========================


Requirements
============

ElephantBlog needs at least:

* Django v1.4 (get it here: https://github.com/django/django)
* FeinCMS v1.5 (get it here: https://github.com/feincms/feincms)


Installation
============

* At this time, there is no prebundled installation file to install via pip or easy_install. So get
the source at: https://github.com/feincms/feincms-elephantblog/

* Make sure to add the ``elephantblog`` to your python path.

* Add ``elephantblog`` to your ``INSTALLED_APPS`` in your settings.py

In your ``application/models.py`` register the blog module and content types::

    from feincms.content.richtext.models import RichTextContent

    from elephantblog.models import Entry

    Entry.register_regions(
        ('main', _('Main content area')),
    )
    Entry.create_content_type(RichTextContent, cleanse=False, regions=('main'))


.. note::

    Of course, you can create all of the content types, that you have for your FeinCMS Page.


Integrating Standalone:
-----------------------

Add the following lines to your urls.py::


    # Elephantblog urls
    urlpatterns += patterns('',
        url(r'^blog/', include('elephantblog.urls')),
    )


run ``manage.py syncdb``.


FeinCMS Integration as ApplicationContent
-----------------------------------------

You can easily add the blog to your FeinCMS Page based app.

Just import and add the ApplicationContent to your Page object::

    from feincms.content.application.models import ApplicationContent

    # init your Page object here

    Page.create_content_type(ApplicationContent, APPLICATIONS=(
            ('elephantblog.urls', 'Blog'),
    ))


Elephantblog also provides a navigation extension for FeinCMS.
Just make sure you have registered the 'navigation' extension on your Page object.

