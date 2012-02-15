=========================================================
ElephantBlog - An extensible Blog Module based on FeinCMS
=========================================================

Every Django Developer has written its own Django-based blog. But most of them have a lot
of features, that you'll never use and never wanted to, or they are just too simple for your
needs, so you'll be quicker writing your own.

Following the principles of FeinCMS, ElephantBlog tries to offer simple and basic blog
functionality, but remains extensible so that you just pick what you need. And if
you don't find an extension, you can quickly write your own and use it with
ElephantBlog.


How it works:
=============

Basically, ElephantBlog just uses what FeinCMS already has in a blog way. A blog way means:
Multiple entries in a timeline. One blogentry is similar to a FeinCMS page: It can have
multiple content types and some meta informations like title, slug, publishing date, ...

If you need more, like comments, tagging, pinging, categories, translations, you name it,
then you can use the bundled extensions or write your own. (and please don't forget
to publish your extensions back to the community).

And obviously, ElephantBlog can also be integrated as application content in your existing
FeinCMS site. But if you want to run a blog only, then you don't have to activate FeinCMS
page module.


Features:
=========

The biggest feature may be that there are only a few features:

* Pretty URLs
* Feed creation
* Time-based publishing
* Based on FeinCMS item editor with the ability to integrate all of those FeinCMS
  content types


Bundled extensions:
-------------------

You can, if you want, activate those extensions:

* Disqus comments
* Pinging
* Categories
* Multilingual support
* Pingback & Trackback support
* ... (more to come, you name it!)


Getting started:
================

If you are not familiar with FeinCMS then you probably want to learn more about FeinCMS:
http://feincms.org

Read the docs: http://feincms-elephantblog.readthedocs.org/en/latest/

Read the source: https://github.com/feincms/feincms-elephantblog
