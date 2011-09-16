from django import template
from django.core.exceptions import FieldError

from feincms.translations import short_language_code

from elephantblog.models import Entry


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