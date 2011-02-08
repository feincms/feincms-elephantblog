#coding=utf-8
from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.template import TemplateSyntaxError
from elephantblog.models import Entry
from django.core.exceptions import FieldError
from django.views.generic import list_detail

register = template.Library()
""" These tags require Django >=1.3 and request context """

@register.simple_tag(takes_context=True)
def get_entries(context, limit):
    try:
        language_code = context['request']._feincms_page.language
        queryset = Entry.objects.active().filter(language=language_code)
    except (AttributeError, FieldError):
        queryset = Entry.objects.active()
    if limit:
        queryset = queryset[:limit]
    context['entries'] = queryset
    return ''


@register.simple_tag(takes_context=True)
def get_frontpage(context):
    try:
        language_code = context['request']._feincms_page.language
        queryset = Entry.objects.active().filter(language=language_code, published__gt=50)
    except (AttributeError, FieldError):
        queryset = Entry.objects.active()
    context['entries'] = queryset
    return ''

""" Legacy Tags for Django 1.2 """

class GetEntries(template.Node):
    def __init__(self, limit):
        self.limit = limit
    def render(self, context):
        try:
            language_code = context['request']._feincms_page.language
            queryset = Entry.objects.active().filter(language=language_code)
        except (AttributeError, FieldError):
            queryset = Entry.objects.active()
        if self.limit:
            queryset = queryset[:self.limit]
        context['entries'] = queryset
        return ''


def do_get_entries(parser, token):
    try:
        tag_name, limit = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return GetEntries(limit)
register.tag('get_entries_legacy', do_get_entries)