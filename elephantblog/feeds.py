from django.conf import settings
from django.contrib.syndication.views import Feed
from django.template.loader import render_to_string
from django.utils.translation import get_language

from elephantblog.models import Entry


if not (hasattr(settings, "BLOG_TITLE") and hasattr(settings, "BLOG_DESCRIPTION")):
    import warnings

    warnings.warn(
        "BLOG_TITLE and/or BLOG_DESCRIPTION not defined in"
        " settings.py. Standard values used for the Feed"
    )


def tryrender(content):
    try:
        return render_to_string(
            "elephantblog/entry_description.html", {"content": content}
        )
    except Exception:  # Required request argument or something else?
        return ""


class EntryFeed(Feed):
    title = getattr(settings, "BLOG_TITLE", "Unnamed")
    link = "/blog/"
    description = getattr(settings, "BLOG_DESCRIPTION", "")

    def items(self):
        if hasattr(Entry, "translation_of"):
            return (
                Entry.objects.active()
                .filter(language=get_language())
                .order_by("-published_on")[:20]
            )
        else:
            return Entry.objects.active().order_by("-published_on")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "".join(tryrender(c) for c in item.content.main)

    def item_pubdate(self, item):
        return item.published_on
