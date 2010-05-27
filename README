A full featrued blog for FeinCMS
================================

Elephantblog is easy to add to FeinCMS and has the following features:

    ⁃   Disqus integration for comments
    ⁃   Pings for new entries
    ⁃   Pretty URLs
    ⁃   Categories
    ⁃   Tagging (optional)
    ⁃   RSS Feed creation
    ⁃   Multilingual (optional)
    ⁃   Time based publishing
    ⁃   Advanced time based publishing (optional)
    ⁃   Pingback and Trackback support (optional)
    ⁃   Spam protection
    ⁃   Admin interface similar to FeinCMS Pages
    ⁃   Additional content type widgets for the Page module

The app is dependent on external django apps. The following apps are required:
    •   Feincms:http://github.com/matthiask/feincms (obviously) 
    •   Pinging:http://github.com/matthiask/pinging.git
    •   Django-disqus:http://github.com/arthurk/django-disqus.git

The following apps are optional but recommended:
    •   Django-tagging
    •   Django-trackback

Note that all comments are managed by Disqus. They are not stored on your server. It is possible to download them as JSON object from the disqus website.

Optional Functions:
Tagging
Allows to add tags to your entries. Tags can be separated by commas or spaces. This function needs to be added as extension and as app.

Trackback
Allows automatic inter-blog communication. Lets you know when someone posted something about your entry on a different website.

Translations
If your blog has entries in different languages, use this extension.

Datepublisher
Lets you set an expiration date to your entries. This is an extension as well.


Installation:

You need a Disqus account: http://www.disqus.com/

Copy the elephantblog dir into your project directory.
Add 'elephantblog' , 'disqus' and 'pinging' to your INSTALLED_APPS in your settings.py
Optionally add 'tagging' and 'trackback' as well.


Add the following lines to settings.py:

PINGING_WEBLOG_NAME = '<your blog name>'
PINGING_WEBLOG_URL = '<your blog url>'
DISQUS_API_KEY = '<api key>'
DISQUS_WEBSITE_SHORTNAME = '<Disqus website shortname>'


In your application/models.py register the blog module and content types:

from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.video.models import VideoContent
from elephantblog.models import Entry as Elephantentry
Elephantentry.register_extensions('translations', 'tags', 'datepublisher') 
Elephantentry.create_content_type(RichTextContent)
MediaFileContent.default_create_content_type(Elephantentry)
Elephantentry.create_content_type(VideoContent)


Add the following lines to your urls.py:

# Elephantblog urls
urlpatterns += patterns('',
    url(r'^blog/', include('elephantblog.urls')),
)


run manage.py syncdb.


Pinging:

The Pinging app uses the management command manage.py blogping to generate the pings for the search engines. Set it up to run as a cron job. 

Here is a list of servers that can be used for pinging: http://www.netlupe.de/2006/08/18/url-zum-pingen-blog-n-ping-urls/






