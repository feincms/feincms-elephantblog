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

Optional packages:

* Pinging_ for search engine pinging.

.. _Pinging: https://github.com/matthiask/pinging

Installation
============

You can install elephantblog using ``pip install feincms-elephantblog``.

* Add ``elephantblog`` to your ``INSTALLED_APPS`` in your ``settings.py``

The first step is to create a new app. As an example, let's name it ``blog``. You can use ``manage.py`` to create it::

    python manage.py startapp blog

Then, add ``elephantblog`` and ``blog`` to your ``INSTALLED_APPS`` in your ``settings.py``::

    INSTALLED_APPS = [
        'blog.apps.BlogConfig',
        'elephantblog',
        # Your other apps,
    ]

In the ``models.py`` file of your ``blog`` app, register the elephantblog module, extensions and
content types::

    from feincms.contents import RichTextContent

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
