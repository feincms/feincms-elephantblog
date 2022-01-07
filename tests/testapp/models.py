from feincms.contents import RichTextContent
from feincms.module.medialibrary.contents import MediaFileContent

from elephantblog.models import Entry


Entry.register_regions(
    ("main", "Main content area"),
)
Entry.register_extensions("feincms.extensions.translations")
Entry.create_content_type(RichTextContent, cleanse=False, regions=("main",))
Entry.create_content_type(MediaFileContent, TYPE_CHOICES=(("default", "default"),))
