.. _extensions:


Pinging
-------

The Pinging app uses the management command manage.py blogping to generate the pings for the search engines. Set it up to run as a cron job.

You need to add the following statements to your settings file::

    BLOG_TITLE = 'My great blog'
    BLOG_BASE_URL = 'http://mysite.com/blog/'

Here is a list of servers that can be used for pinging: `<http://www.netlupe.de/2006/08/18/url-zum-pingen-blog-n-ping-urls/>`_


