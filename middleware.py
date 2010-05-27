from django.utils.translation import activate

import re

LANGUAGE_RE = re.compile(r'^/(de|en)/')

class SetLocaleFromPath(object):
    def process_request(self, request):
        matches = LANGUAGE_RE.match(request.path)
        if matches:
            activate(matches.group(1))

"""
'django.middleware.locale.LocaleMiddleware',
'elephantblog.middleware.SetLocaleFromPath', 
"""