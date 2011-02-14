.. _installation:

=========================
Installation instructions
=========================

Installation
============

You can sign up for a Disqus account at: `http://www.disqus.com/`

Copy the elephantblog dir into your project directory.
Add 'elephantblog' , 'disqus' and 'pinging' to your INSTALLED_APPS in your settings.py
Optionally add 'tagging' and 'trackback' as well.

.. note::

    Disqus is not required. If you are not using it, remove the disqus tags in the template.


Add the following lines to settings.py::

    PINGING_WEBLOG_NAME = '<your blog name>'
    PINGING_WEBLOG_URL = '<your blog url>'
    DISQUS_API_KEY = '<api key>'
    DISQUS_WEBSITE_SHORTNAME = '<Disqus website shortname>'


In your application/models.py register the blog module and content types::

    from feincms.content.richtext.models import RichTextContent
    from feincms.content.medialibrary.models import MediaFileContent
    from feincms.content.video.models import VideoContent
    from elephantblog.models import Entry as Elephantentry
    Elephantentry.register_extensions('translations', 'tags', 'datepublisher') 
    Elephantentry.create_content_type(RichTextContent)
    MediaFileContent.default_create_content_type(Elephantentry)
    Elephantentry.create_content_type(VideoContent)


Add the following lines to your urls.py::


    # Elephantblog urls
    urlpatterns += patterns('',
        url(r'^blog/', include('elephantblog.urls')),
    )

.. note::

    When using the blog within an application content use the url file 'appcontenturls.py'.

run manage.py syncdb.


Pinging
-------

The Pinging app uses the management command manage.py blogping to generate the pings for the search engines. Set it up to run as a cron job. 

Here is a list of servers that can be used for pinging: `<http://www.netlupe.de/2006/08/18/url-zum-pingen-blog-n-ping-urls/>`_


