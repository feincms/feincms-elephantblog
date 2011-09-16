from django import template

from elephantblog.models import Category, Entry


register = template.Library()


@register.assignment_tag
def elephantblog_categories():
    return Category.objects.all()


@register.assignment_tag
def elephantblog_archive_months():
    return Entry.objects.active().dates('published_on', 'month', 'DESC')
