from django.utils.translation import ugettext_lazy as _

from feincms.module.page.extensions.navigation import (NavigationExtension,
    PagePretender)

from elephantblog.models import Category


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
