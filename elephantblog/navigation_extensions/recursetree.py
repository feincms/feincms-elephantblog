"""optimized for use with the feincms_nav and recursetree template tag."""

from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from .common import Category, NavigationExtension, PagePretender, all_months, date_tree


class RBlogDateNavigationExtension(NavigationExtension):
    """
    Special version optimized for recursetree template tag
    """

    name = gettext_lazy("Blog date")

    def children(self, page, **kwargs):
        for year, months in date_tree():

            def return_months(year=year, months=months):
                for month in months:
                    yield PagePretender(
                        title="{}".format(_(all_months[month - 1].strftime("%B"))),
                        url=f"{page.get_absolute_url()}{year:04d}/{month:02d}/",
                        tree_id=page.tree_id,
                        level=page.level + 2,
                        language=getattr(page, "language", settings.LANGUAGE_CODE),
                        slug=f"{year:04d}/{month:02d}",
                        lft=0,
                        rght=0,
                        _mptt_meta=page._mptt_meta,
                    )

            yield PagePretender(
                title=f"{year}",
                url=f"{page.get_absolute_url()}{year}/",
                tree_id=page.tree_id,
                language=getattr(page, "language", settings.LANGUAGE_CODE),
                level=page.level + 1,
                slug=f"{year}",
                parent=page,
                parent_id=page.id,
                get_children=return_months,
                lft=page.lft + 1,
                rght=len(months) + 1,
                _mptt_meta=page._mptt_meta,
            )


class RCategoryAndDateNavigationExtension(NavigationExtension):
    name = gettext_lazy("Blog category and date")

    def children(self, page, **kwargs):
        all_categories = Category.objects.all()

        def return_children():
            for category in all_categories:
                yield PagePretender(
                    title=category.translation.title,
                    url=f"{page.get_absolute_url()}category/{category.translation.slug}/",
                    tree_id=page.tree_id,
                    level=page.level + 2,
                    language=getattr(page, "language", settings.LANGUAGE_CODE),
                    slug=category.translation.slug,
                    lft=0,
                    rght=0,
                    _mptt_meta=page._mptt_meta,
                )

        yield PagePretender(
            title=_("Categories"),
            url="./",
            tree_id=page.tree_id,
            level=page.level + 1,
            parent=page,
            parent_id=page.id,
            slug="",
            language=getattr(page, "language", settings.LANGUAGE_CODE),
            get_children=return_children,
            lft=page.lft + 1,
            rght=len(all_categories) + 1,
            _mptt_meta=page._mptt_meta,
        )

        def return_dates():
            for year, months in date_tree():

                def return_months(year=year, months=months):
                    for month in months:
                        yield PagePretender(
                            title="{}".format(_(all_months[month - 1].strftime("%B"))),
                            url=f"{page.get_absolute_url()}{year:04d}/{month:02d}/",
                            tree_id=page.tree_id,
                            level=page.level + 3,
                            language=getattr(page, "language", settings.LANGUAGE_CODE),
                            slug=f"{year:04d}/{month:02d}",
                        )

                yield PagePretender(
                    title=f"{year}",
                    url=f"{page.get_absolute_url()}{year}/",
                    tree_id=page.tree_id,
                    level=page.level + 2,
                    slug=f"{year}",
                    language=getattr(page, "language", settings.LANGUAGE_CODE),
                    get_children=return_months,
                )

        yield PagePretender(
            title=_("Archive"),
            url="./",
            tree_id=page.tree_id,
            level=page.level + 1,
            slug="",
            parent=page,
            parent_id=page.id,
            language=getattr(page, "language", settings.LANGUAGE_CODE),
            get_children=return_dates,
            lft=0,
            rght=0,
            _mptt_meta=page._mptt_meta,
        )
