from django.utils.translation import ugettext_lazy as _

from feincms.module.page.extensions.navigation import (NavigationExtension,
    PagePretender)

from elephantblog.models import Category, Entry
import datetime

from django.utils.datastructures import  SortedDict

class BlogCategoriesNavigationExtension(NavigationExtension):
    """
    Navigation extension for FeinCMS which lists all available categories
    """

    name = _('blog categories')

    def children(self, page, **kwargs):
        for category in Category.objects.all():
            yield PagePretender(
                title=category.translation.title,
                url='%scategory/%s/' % (page.get_absolute_url(), category.translation.slug),
                tree_id=page.tree_id, # pretty funny tree hack
                lft=0,
                rght=0,
                slug=category.translation.slug,
                )

class BlogDateNavigationExtension(NavigationExtension):
    """
    Navigation extension for FeinCMS which shows a year and month Breakdown:
    2012
        April
        March
        February
        January
    2011
    2010
    """
    name = _('blog date')

    def __init__(self, *args, **kwargs):
        super(BlogDateNavigationExtension, self).__init__(*args, **kwargs)
        self.months = [datetime.date(2008, i, 1) for i in range(1,13)]

    def date_of_first_entry(self):
        entry = Entry.objects.filter(is_active=True).order_by('published_on')[0]
        return entry.published_on.date()

    def date_tree(self):
        """ returns a dict in the form {2012: [1,2,3,4,5,6], 2011: [10,11,12]} """
        today = datetime.date.today()
        first_day = self.date_of_first_entry()
        years = range(first_day.year, today.year+1)
        date_tree = SortedDict((year, range(1,13)) for year in years)
        for year, months in date_tree.items():
            if year == first_day.year:
                date_tree[year] = months[(first_day.month-1):]
            if year == today.year:
                # list might be missing some elements because it is also the first year.
                months_this_year = range(1, today.month+1)
                date_tree[year] = [m for m in date_tree[year] if m in months_this_year]
        return date_tree.items()

    def children(self, page, **kwargs):
        for year, months in self.date_tree():
            yield PagePretender(
                title=u'%s' % year,
                url='%s%s/' % (page.get_absolute_url(), year),
                tree_id=page.tree_id, # pretty funny tree hack
                lft=0,
                rght=len(months)+1,
                level=page.level+1,
                slug='%s' % year,
                )
            for month in months:
                yield PagePretender(
                    title=u'%s' % self.months[month-1].strftime('%B'),
                    url='%s%04d/%02d/' % (page.get_absolute_url(), year, month),
                    tree_id=page.tree_id, # pretty funny tree hack
                    lft=0,
                    rght=0,
                    level=page.level+2,
                    slug='%04d/%02d' % (year, month),
                )