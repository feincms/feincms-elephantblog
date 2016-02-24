from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
import datetime

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.extensions.navigation import (
    NavigationExtension, PagePretender)

from elephantblog.models import Entry, Category


all_months = [datetime.date(2008, i, 1) for i in range(1, 13)]


def date_of_first_entry():
    entry = Entry.objects.filter(is_active=True).order_by('published_on')[0]
    return entry.published_on.date()


def date_tree():
    """ returns a dict in the form {2012: [1,2,3,4,5,6], 2011: [10,11,12]} """
    today = datetime.date.today()
    first_day = date_of_first_entry()
    years = range(today.year, first_day.year - 1, -1)
    date_tree = OrderedDict((year, range(1, 13)) for year in years)
    for year, months in date_tree.items():
        if year == first_day.year:
            date_tree[year] = months[first_day.month - 1:]
        if year == today.year:
            # list might be missing some elements because it is also the
            # first year.
            months_this_year = range(1, today.month + 1)
            date_tree[year] = [
                m for m in date_tree[year] if m in months_this_year]
    return date_tree.items()


class BlogCategoriesNavigationExtension(NavigationExtension):
    """
    Navigation extension for FeinCMS which lists all available categories
    """

    name = _('blog categories')

    def children(self, page, **kwargs):
        categories = Category.objects.all()
        for category in categories:
            yield PagePretender(
                title=category.translation.title,
                url='%scategory/%s/' % (
                    page.get_absolute_url(),
                    category.translation.slug),
                tree_id=page.tree_id,
                level=page.level + 1,
                language=getattr(page, 'language', settings.LANGUAGE_CODE),
                slug=category.translation.slug,
                parent=page,
                parent_id=page.id,
                lft=page.lft,
                rght=page.rght,
                _mptt_meta=getattr(page, '_mptt_meta', None),
            )
