from __future__ import absolute_import, unicode_literals

from django import template
from django.core.exceptions import FieldError
from django.utils.translation import get_language

from elephantblog.models import Entry
from elephantblog.utils import entry_list_lookup_related, same_category_entries


register = template.Library()


@register.simple_tag(takes_context=True)
def get_entries(context, limit):
    try:
        queryset = Entry.objects.active().filter(
            language=get_language())
    except (AttributeError, FieldError):
        queryset = Entry.objects.active()

    if limit:
        queryset = queryset[:limit]

    context['entries'] = queryset
    return ''


@register.simple_tag(takes_context=True)
def get_frontpage(context, category=None):
    queryset = Entry.objects.featured()

    try:
        queryset = queryset.filter(language=get_language())
    except (AttributeError, FieldError):
        pass

    if category:
        queryset = queryset.filter(
            categories__translations__title=category).distinct()

    context['entries'] = queryset
    return ''


@register.simple_tag(takes_context=True)
def get_others(context, number=3, same_category=True, featured_only=False):
    """ This tag can be used on an entry detail page to tease
        other related entries
    """
    if same_category:
        entries = same_category_entries(context['object'])
    else:
        entries = Entry.objects.exclude(pk=context['object'].pk)
    if featured_only:
        entries.filter(is_featured=True)

    entries = entries[:number]
    entries = entries.transform(entry_list_lookup_related)
    context['others'] = entries
    return ''
