from __future__ import absolute_import, unicode_literals

from django import template
from django.contrib.auth import get_user_model
from django.db.models import FieldDoesNotExist
from django.utils.translation import get_language

from elephantblog.models import Category, Entry
from elephantblog.utils import entry_list_lookup_related


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
def elephantblog_archive_years():
    """
    Assigns a list of years with active entries to a template variable of
    your choice. Especially useful to generate archive links::

        {% elephantblog_archive_years as years %}
        <ul>
        {% for year in years %}
            <li>
                <a href="{% url 'elephantblog_entry_archive_year'
                        year=year.year %}">
                    {{ year.year }}
                </a>
            </li>
        {% endfor %}
        </ul>

    (Wrapped for legibility, the ``{% url %}`` template tag must be on a
    single line.)
    """
    return Entry.objects.active().datetimes(
        'published_on', 'year', 'DESC')


@register.assignment_tag
def elephantblog_archive_months():
    """
    Assigns a list of months with active entries to a template variable of
    your choice. Especially useful to generate archive links::

        {% elephantblog_archive_months as months %}
        <ul>
        {% for month in months %}
            <li>
                <a href="{% url 'elephantblog_entry_archive_month'
                        year=month.year
                        month=month|date:"m" %}">
                    {{ month|date:"F Y" }}
                </a>
            </li>
        {% endfor %}
        </ul>

    (Wrapped for legibility, the ``{% url %}`` template tag must be on a
    single line.)
    """
    return Entry.objects.active().datetimes(
        'published_on', 'month', 'DESC')


@register.assignment_tag
def elephantblog_entries(limit=10,
                         featured_only=False,
                         active_language_only=True,
                         category=None):
    """
    Usage::

        {% elephantblog_entries limit=2 featured_only=True as entries %}

    or::

        {% elephantblog_entries limit=10 as entries %}

    or::

        {% elephantblog_entries active_language_only=False as entries %}

    or::

        {% elephantblog_entries category=some_category as entries %}
    """

    queryset = Entry.objects.active()
    if featured_only:
        queryset = queryset.filter(is_featured=True)

    try:
        queryset.model._meta.get_field('language')
    except FieldDoesNotExist:
        pass
    else:
        if active_language_only:
            queryset = queryset.filter(language=get_language())

    if category is not None:
        queryset = queryset.filter(categories=category)

    return queryset.transform(entry_list_lookup_related)[:limit]


@register.assignment_tag
def elephantblog_authors():
    return get_user_model().objects.filter(
        id__in=Entry.objects.active().order_by().values('author'),
    )
