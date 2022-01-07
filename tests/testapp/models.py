from elephantblog.models import Entry


try:
    from feincms.contents import RichTextContent
    from feincms.module.medialibrary.contents import MediaFileContent
except ImportError:  # FeinCMS<2
    from feincms.content.medialibrary.models import MediaFileContent
    from feincms.content.richtext.models import RichTextContent


Entry.register_regions(
    ("main", "Main content area"),
)

try:
    # FeinCMS 2.0
    import feincms.extensions.translations  # noqa
except ImportError:
    Entry.register_extensions("feincms.module.extensions.translations")
else:
    Entry.register_extensions("feincms.extensions.translations")

Entry.create_content_type(RichTextContent, cleanse=False, regions=("main",))
Entry.create_content_type(MediaFileContent, TYPE_CHOICES=(("default", "default"),))
