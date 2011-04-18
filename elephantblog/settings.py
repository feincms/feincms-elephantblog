"""
Default settings for elephantblog. to change these settings, simply set the 
setting in your projects settings.py
"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# How blog comments should be made. Options for now are 'disqus', 
# 'django-comments' or None
BLOG_COMMENTS = getattr(settings, 'BLOG_COMMENTS', None)

# Title of the Blog, currently used for Feed title
BLOG_TITLE = getattr(settings, 'BLOG_TITLE', _('title undefined'))

# Description of the blog, currently used for feed description
BLOG_DESCRIPTION = getattr(settings, 'BLOG_DESCRIPTION', 
                           _('description undefined'))

# Set pagination for elephantblog.views.entry_list, None to use default from 
# entry_dict
BLOG_LIST_PAGINATION = getattr(settings, 'BLOG_LIST_PAGINATION', None)