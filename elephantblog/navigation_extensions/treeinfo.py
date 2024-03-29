from django.utils.translation import gettext as _, gettext_lazy

from .common import Category, NavigationExtension, PagePretender, all_months, date_tree


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

    name = gettext_lazy("Blog date")

    def children(self, page, **kwargs):
        for year, months in date_tree():
            yield PagePretender(
                title="%s" % year,
                url=f"{page.get_absolute_url()}{year}/",
                tree_id=page.tree_id,
                lft=0,
                rght=len(months) + 1,
                level=page.level + 1,
                slug="%s" % year,
            )
            for month in months:
                yield PagePretender(
                    title="%s" % _(all_months[month - 1].strftime("%B")),
                    url="%s%04d/%02d/" % (page.get_absolute_url(), year, month),
                    tree_id=page.tree_id,
                    lft=0,
                    rght=0,
                    level=page.level + 2,
                    slug="%04d/%02d" % (year, month),
                )


class CategoryAndDateNavigationExtension(NavigationExtension):
    name = gettext_lazy("Blog category and date")

    def children(self, page, **kwargs):
        all_categories = Category.objects.all()
        yield PagePretender(
            title=_("Categories"),
            url="#",
            tree_id=page.tree_id,
            lft=0,
            rght=len(all_categories) + 1,
            level=page.level,
            slug="#",
        )

        for category in all_categories:
            yield PagePretender(
                title=category.translation.title,
                url="%scategory/%s/"
                % (page.get_absolute_url(), category.translation.slug),
                tree_id=page.tree_id,
                lft=0,
                rght=0,
                level=page.level + 1,
                slug=category.translation.slug,
            )

        yield PagePretender(
            title=_("Archive"),
            url="#",
            tree_id=page.tree_id,
            lft=0,
            rght=500,  # does it really matter?
            level=page.level,
            slug="#",
        )

        for year, months in date_tree():
            yield PagePretender(
                title="%s" % year,
                url=f"{page.get_absolute_url()}{year}/",
                tree_id=page.tree_id,
                lft=0,
                rght=len(months) + 1,
                level=page.level + 1,
                slug="%s" % year,
            )

            for month in months:
                yield PagePretender(
                    title="%s" % _(all_months[month - 1].strftime("%B")),
                    url="%s%04d/%02d/" % (page.get_absolute_url(), year, month),
                    tree_id=page.tree_id,
                    lft=0,
                    rght=0,
                    level=page.level + 2,
                    slug="%04d/%02d" % (year, month),
                )
