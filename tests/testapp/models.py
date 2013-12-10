# -*- coding:utf-8 -*-
from elephantblog.models import Entry
from feincms.content.richtext.models import RichTextContent

Entry.register_regions(
    ('main', 'Main content area'),
)
Entry.create_content_type(RichTextContent, cleanse=False, regions=('main',))
