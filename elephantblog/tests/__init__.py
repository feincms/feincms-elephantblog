"""
To use the test suite you can use the included test project. It's a very basic
django app that is fully functional.

1. Create a virtualenv
2. run ``pip install -r requirements_dev.txt to install the testing tools``
3. run the tests: ``./elephantblog/tests/testapp/manage.py test  elephantblog``
"""

from .test_translations import *
from .test_timezones import *
from .test_archive_views import *