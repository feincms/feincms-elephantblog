""" optimized for use with the feincms_nav and recursetree template tag. """

from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.utils.translation import ugettext as _, ugettext_lazy

from .common import (
    Category, NavigationExtension, PagePretender, all_months, date_tree)


class RBlogDateNavigationExtension(NavigationExtension):
    """
    Special version optimized for recursetree template tag
    """
    name = ugettext_lazy('Blog date')

    def children(self, page, **kwargs):
        for year, months in date_tree():
            def return_months():
                for month in months:
                    yield PagePretender(
                        title='%s' % _(all_months[month - 1].strftime('%B')),
                        url='%s%04d/%02d/' % (
                            page.get_absolute_url(), year, month),
                        tree_id=page.tree_id,
                        level=page.level + 2,
                        language=getattr(
                            page, 'language', settings.LANGUAGE_CODE),
                        slug='%04d/%02d' % (year, month),
                        lft=0,
                        rght=0,
                        _mptt_meta=page._mptt_meta,
                    )

            yield PagePretender(
                title='%s' % year,
                url='%s%s/' % (page.get_absolute_url(), year),
                tree_id=page.tree_id,
                language=getattr(page, 'language', settings.LANGUAGE_CODE),
                level=page.level + 1,
                slug='%s' % year,
                parent=page,
                parent_id=page.id,
                get_children=return_months,
                lft=page.lft + 1,
                rght=len(months) + 1,
                _mptt_meta=page._mptt_meta,
            )


class RCategoryAndDateNavigationExtension(NavigationExtension):
    name = ugettext_lazy('Blog category and date')

    def children(self, page, **kwargs):
        all_categories = Category.objects.all()

        def return_children():
            for category in all_categories:
                yield PagePretender(
                    title=category.translation.title,
                    url='%scategory/%s/' % (
                        page.get_absolute_url(), category.translation.slug),
                    tree_id=page.tree_id,
                    level=page.level + 2,
                    language=getattr(page, 'language', settings.LANGUAGE_CODE),
                    slug=category.translation.slug,
                    lft=0,
                    rght=0,
                    _mptt_meta=page._mptt_meta,
                )

        yield PagePretender(
            title=_('Categories'),
            url='./',
            tree_id=page.tree_id,
            level=page.level + 1,
            parent=page,
            parent_id=page.id,
            slug='',
            language=getattr(page, 'language', settings.LANGUAGE_CODE),
            get_children=return_children,
            lft=page.lft + 1,
            rght=len(all_categories) + 1,
            _mptt_meta=page._mptt_meta,
        )

        def return_dates():
            for year, months in date_tree():
                def return_months():
                    for month in months:
                        yield PagePretender(
                            title='%s' % _(
                                all_months[month - 1].strftime('%B')),
                            url='%s%04d/%02d/' % (
                                page.get_absolute_url(), year, month),
                            tree_id=page.tree_id,
                            level=page.level + 3,
                            language=getattr(
                                page, 'language', settings.LANGUAGE_CODE),
                            slug='%04d/%02d' % (year, month),
                        )
                yield PagePretender(
                    title='%s' % year,
                    url='%s%s/' % (page.get_absolute_url(), year),
                    tree_id=page.tree_id,
                    level=page.level + 2,
                    slug='%s' % year,
                    language=getattr(page, 'language', settings.LANGUAGE_CODE),
                    get_children=return_months,
                )

        yield PagePretender(
            title=_('Archive'),
            url='./',
            tree_id=page.tree_id,
            level=page.level + 1,
            slug='',
            parent=page,
            parent_id=page.id,
            language=getattr(page, 'language', settings.LANGUAGE_CODE),
            get_children=return_dates,
            lft=0,
            rght=0,
            _mptt_meta=page._mptt_meta,
        )
