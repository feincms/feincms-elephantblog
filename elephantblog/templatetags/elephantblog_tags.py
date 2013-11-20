from django import template

from elephantblog.models import Category, Entry


register = template.Library()


@register.assignment_tag
def elephantblog_categories(show_empty_categories=False):
    """
    Assigns the list of categories to a template variable of your choice. The
    default is to only return categories which have at least one blog entry::

        {% elephantblog_categories as categories %}

    It's also possible to return all categories::

        {% elephantblog_categories show_empty_categories=True as categories %}
    """
    if show_empty_categories:
        return Category.objects.all()
    return Category.objects.exclude(blogentries__isnull=True)


@register.assignment_tag
def elephantblog_archive_months():
    return Entry.objects.active().dates('published_on', 'month', 'DESC')
