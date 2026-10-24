.. _changelog:

Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

v26.10.0 (2026-10-24)
~~~~~~~~~~~~~~~~~~~~~

- Dropped support for Python 3.8 and 3.9. Python 3.10 or better is required
  now, like in FeinCMS.
- Added Django 5.2, 6.0 and 6.1 and Python 3.11 up to 3.15 support.
- Fixed ``AttributeError`` when rendering empty inherited regions of entries.
  Entries do not inherit content from anywhere.
- Fixed the detail view overwriting ``first_richtext`` and ``first_image``
  assigned by a custom ``BLOG_LOOKUP_CLASS``. ``DateDetailView.lookup_related``
  has been removed; the lookup class is used for detail views as well now.
  Documented the ``BLOG_LOOKUP_CLASS`` setting.


`v22.0.0`_ (2022-01-07)
~~~~~~~~~~~~~~~~~~~~~~~

- Added pre-commit.
- Dropped compatibility with Python < 3.9, Django < 3.2.
- Made the tags extension add tags to the ``list_filter``.


`v1.3.0`_ (2020-01-29)
~~~~~~~~~~~~~~~~~~~~~~

- Changed contents to return a ``(template, context)`` tuple from their
  render methods. The minimum FeinCMS version supporting this is 1.15.


`v1.2.0`_ (2020-01-21)
~~~~~~~~~~~~~~~~~~~~~~

- Reformatted the code using black.
- Updated the code to work with Django 2 and 3.



.. _v1.2.0: https://github.com/feincms/feincms-elephantblog/compare/v1.1.0...v1.2.0
.. _v1.3.0: https://github.com/feincms/feincms-elephantblog/compare/v1.2.0...v1.3.0
.. _v22.0.0: https://github.com/feincms/feincms-elephantblog/compare/v1.3.0...v22.0.0
.. _Next version: https://github.com/feincms/feincms-elephantblog/compare/v22.0.0...master
