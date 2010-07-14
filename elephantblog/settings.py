"""
Default settings for elephantblog. to change these settings, simply set the 
setting in your projects settings.py
"""
from django.conf import settings

# How blog comments should be made. Options for now are 'disqus', 
# 'django-comments' or None
BLOG_COMMENTS = getattr(settings, 'BLOG_COMMENTS', None)