"""
Default settings for elephantblog. to change these settings, simply set the
setting in your projects settings.py
"""

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

#: Title of the Blog, currently used for Feed title
BLOG_TITLE = getattr(settings, 'BLOG_TITLE', _('title undefined'))

#: Description of the blog, currently used for feed description
BLOG_DESCRIPTION = getattr(settings, 'BLOG_DESCRIPTION',
                           _('description undefined'))