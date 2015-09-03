# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals

from elephantblog.models import Entry

try:
    from feincms.contents import RichTextContent, MediaFileContent
except ImportError:
    from feincms.content.richtext.models import RichTextContent
    from feincms.content.medialibrary.models import MediaFileContent


Entry.register_regions(
    ('main', 'Main content area'),
)
Entry.register_extensions('feincms.module.extensions.translations',)
Entry.create_content_type(RichTextContent, cleanse=False, regions=('main',))
Entry.create_content_type(
    MediaFileContent,
    TYPE_CHOICES=(('default', 'default'),))
