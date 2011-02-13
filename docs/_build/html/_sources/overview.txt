.. _overview:

========
Overview
========

A full featured blog for FeinCMS
================================

Elephantblog is easy to add to FeinCMS and has the following features:

* Disqus integration for comments
* Pings for new entries
* Pretty URLs
* Categories
* Tagging (optional)
* RSS Feed creation
* Multilingual (optional)
* Time based publishing
* Advanced time based publishing (optional)
* Pingback and Trackback support (optional)
* Spam protection
* Admin interface similar to FeinCMS Pages
* Additional content type widgets for the Page module

The app is dependent on external django apps. The following apps are required:

* feincms: `<http://github.com/matthiask/feincms>`_ (obviously) 
* pinging: `<http://github.com/matthiask/pinging>`_
* django-disqus: `<http://github.com/arthurk/django-disqus>`_

The following apps are optional but recommended:

* Django-tagging
* Django-trackback

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
