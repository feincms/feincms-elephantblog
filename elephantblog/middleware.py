"""
Middleware which sets the current language based on the start of the path

Add this middleware to ``MIDDLEWARE_CLASSES`` right after the
``LocaleMiddleware``::

    'django.middleware.locale.LocaleMiddleware',
    'elephantblog.middleware.SetLocaleFromPath',
"""

import re

from django.utils.translation import activate

LANGUAGE_RE = re.compile(r'^/(de|en)/')


class SetLocaleFromPath(object):
    def process_request(self, request):
        matches = LANGUAGE_RE.match(request.path)
        if matches:
            activate(matches.group(1))
