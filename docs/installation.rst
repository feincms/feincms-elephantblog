.. _installation:

=========================
Installation instructions
=========================


Requirements
============

ElephantBlog needs at least:

* Django v1.4 (get it here: https://github.com/django/django)
* FeinCMS v1.7 (get it here: https://github.com/feincms/feincms)
* TinyMCE_ or any other Richtext editor. TinyMCE goes in /media/js/tiny_mce.

.. _TinyMCE: http://www.tinymce.com/download/download.php

Installation
============

You can install elephantblog using ``pip install feincms-elephantblog``.
It is also recommended to use a HTML sanitizer for rich text content,
e.g. ``pip install html-sanitizer``

* Add ``elephantblog`` to your ``INSTALLED_APPS`` in your ``settings.py``

The first step is to create a new app. As an example, let's name it ``blog``. You can use ``manage.py`` to create it::

    python manage.py startapp blog

Then, add ``elephantblog`` and ``blog`` to your ``INSTALLED_APPS`` in your ``settings.py``::

    INSTALLED_APPS = [
        'blog.apps.BlogConfig',
        'elephantblog',
        # Your other apps, e.g. 'feincms.module.medialibrary' etc.
    ]

In the ``models.py`` file of your ``blog`` app, register the elephantblog module, extensions and
content types::

    from django.utils.translation import gettext_lazy as _
    from feincms.contents import RichTextContent
    from html_sanitizer.django import get_sanitizer

    from elephantblog.models import Entry

    Entry.register_extensions(
        'feincms.module.extensions.datepublisher',
        'feincms.module.extensions.translations',
    )
    Entry.register_regions(
        ('main', _('Main content area')),
    )
    Entry.create_content_type(
        RichTextContent,
        cleanse=get_sanitizer().sanitize,
        regions=('main',),
    )


.. note::

    Of course, you can create all of the content types that you have for your
    FeinCMS Page.

Migrations
----------

Specify the migration modules of your ``blog`` app to your ``MIGRATION_MODULES`` in your ``settings.py`` file::

    MIGRATION_MODULES = {
        'category': 'blog.category_migrations',
        'categorytranslation': 'blog.categorytranslation_migrations',
        'entry': 'blog.entry_migrations',
    }

Create an empty migration file for ``elephantblog``::

    python manage.py makemigrations --empty elephantblog

Perform the migration for ``elephantblog``::

    python manage.py migrate elephantblog

Once you will be finished with the integration (see below) perform the migration of your ``blog`` app by running again::

    python manage.py makemigrations

and::

    python manage.py migrate

Integrating Standalone:
-----------------------

Add the following lines to your urls.py::

    from django.urls import include, url

    # Elephantblog urls
    urlpatterns += [
        url(r'^blog/', include('elephantblog.urls')),
    ]

If you're using the ``translations`` extension, and don't want to have your
entries filtered by language use this snippet instead::

    from django.urls import include, url
    from elephantblog.urls import elephantblog_patterns

    urlpatterns += [
        url(
            r'^blog/',
            include(elephantblog_patterns(
                list_kwargs={'only_active_language': False },
            )),
        ),
    ]


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

    Page.register_extensions('feincms.module.page.extensions.navigation',)


Settings
--------

You can set the number of entries per page with the following setting::

    BLOG_PAGINATE_BY = 10

The list and detail views assign ``first_richtext`` and ``first_image`` to
entries, using ``RichTextContent`` and ``MediaFileContent``. If you're using
other content types, subclass ``elephantblog.transforms.BaseLookup``,
implement ``lookup(entry_qs)`` and point the following setting to your
class::

    BLOG_LOOKUP_CLASS = "blog.transforms.MyLookup"


Feed
----

The feed at ``feed/`` renders the ``main`` region of each entry using the
``elephantblog/entry_description.html`` template. Contents are rendered
without access to the current request, and contents which raise an exception
while rendering are skipped.

If your contents need the request while rendering the feed, make it available
to them using a `context variable
<https://docs.python.org/3/library/contextvars.html>`__ (which, unlike a
thread-local, also works in async code) and use your own subclass of the
feed::

    from contextvars import ContextVar

    from elephantblog.feeds import EntryFeed

    current_request = ContextVar("current_request", default=None)

    class RequestEntryFeed(EntryFeed):
        def __call__(self, request, *args, **kwargs):
            token = current_request.set(request)
            try:
                return super().__call__(request, *args, **kwargs)
            finally:
                current_request.reset(token)

Your contents can then use ``current_request.get()`` in their ``render``
methods. Remember to add the feed to your URLconf yourself, before including
``elephantblog.urls``.

See `pull request #1
<https://github.com/matthiask/feincms-elephantblog/pull/1>`__ for the
discussion.
