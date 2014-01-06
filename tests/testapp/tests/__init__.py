"""
To use the test suite you can use the included test project. It's a very basic
django app that is fully functional.

1. Create a virtualenv
2. run ``pip install -r requirements.txt to install the testing tools``
3. run the tests: ``manage.py test testapp``
"""

from __future__ import absolute_import, unicode_literals

from .test_translations import *  # noqa
from .test_timezones import *  # noqa
from .test_archive_views import *  # noqa
from .test_templatetags import *  # noqa
from .test_feed import *  # noqa
from .test_contents import *  # noqa
from .test_admin import *  # noqa
from .test_sitemap import *  # noqa
