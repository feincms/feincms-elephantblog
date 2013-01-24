from django import template
from django.core.exceptions import FieldError

from feincms.translations import short_language_code

from elephantblog.models import Entry
from elephantblog.utils import entry_list_lookup_related, same_category_entries


register = template.Library()


@register.simple_tag(takes_context=True)
def get_entries(context, limit):
    try:
        queryset = Entry.objects.active().filter(language=short_language_code())
    except (AttributeError, FieldError):
        queryset = Entry.objects.active()

    if limit:
        queryset = queryset[:limit]

    context['entries'] = queryset
    return u''


@register.simple_tag(takes_context=True)
def get_frontpage(context, category=None):
    try:
        queryset = Entry.objects.featured().filter(language=short_language_code())
    except (AttributeError, FieldError):
        queryset = Entry.objects.featured()

    if category:
        queryset = queryset.filter(categories__translations__title=category).distinct()

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