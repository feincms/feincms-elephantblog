from django import template

from elephantblog.models import Category, Entry
from elephantblog.utils import calculate_cloud, get_usage, LOGARITHMIC, LINEAR

register = template.Library()


@register.assignment_tag
def elephantblog_categories():
    return Category.objects.all()


@register.assignment_tag
def elephantblog_archive_months():
    """
    Returns datetime objects of months that contains some entries.
    """
    return Entry.objects.active().dates('published_on', 'month', 'DESC')

@register.assignment_tag
def elephantblog_archive_years():
    """
    Returns datetime objects of years that contains some entries.
    """
    return Entry.objects.active().dates('published_on', 'year', 'DESC')


_distribution_mapping = {'LINEAR' : LINEAR, 'LOGARITHMIC' : LOGARITHMIC}

@register.assignment_tag
def elephantblog_tag_cloud(**kwargs):
    """
    Retrieves used categories and calculates sizes of font used
    based on usage count of particular category. Used for tag cloud.
    """
    steps = kwargs.get('steps', 4)
    distribution = kwargs.get('distribution', 'LINEAR')
    categories = get_usage(Category, counts=True)
    return calculate_cloud(categories, steps, _distribution_mapping[distribution])