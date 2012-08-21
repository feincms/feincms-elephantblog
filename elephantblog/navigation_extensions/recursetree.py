""" optimized for use with the feincms_nav and recursetree template tag. """
from django.utils.translation import ugettext_lazy as _, ugettext

from .common import *


class RBlogDateNavigationExtension(NavigationExtension):
    """
    Special version optimized for recursetree template tag
    """
    name = _('Blog date')

    def children(self, page, **kwargs):

        for year, months in date_tree():
            def return_months():
                for month in months:
                    yield PagePretender(
                        title=u'%s' % ugettext(all_months[month-1].strftime('%B')),
                        url='%s%04d/%02d/' % (page.get_absolute_url(), year, month),
                        tree_id=page.tree_id, # pretty funny tree hack
                        level=page.level+2,
                        language=getattr(page, 'language', settings.LANGUAGE_CODE),
                        slug='%04d/%02d' % (year, month),
                    )
            yield PagePretender(
                title=u'%s' % year,
                url='%s%s/' % (page.get_absolute_url(), year),
                tree_id=page.tree_id, # pretty funny tree hack
                language=getattr(page, 'language', settings.LANGUAGE_CODE),
                level=page.level+1,
                slug='%s' % year,
                parent=page,
                get_children=return_months,
                )


class RCategoryAndDateNavigationExtension(NavigationExtension):
    name = _('Blog category and date')

    def children(self, page, **kwargs):
        all_categories = Category.objects.all()

        def return_children():
            for category in all_categories:
                yield PagePretender(
                    title=category.translation.title,
                    url='%scategory/%s/' % (page.get_absolute_url(), category.translation.slug),
                    tree_id=page.tree_id, # pretty funny tree hack
                    level=page.level+2,
                    language=getattr(page, 'language', settings.LANGUAGE_CODE),
                    slug=category.translation.slug,
                    )

        yield PagePretender(
            title=_('Categories'),
            url='#',
            tree_id=page.tree_id, # pretty funny tree hack
            level=page.level+1,
            parent=page,
            slug='#',
            language=getattr(page, 'language', settings.LANGUAGE_CODE),
            get_children=return_children,
            )

        def return_dates():
            for year, months in date_tree():
                def return_months():
                    for month in months:
                        yield PagePretender(
                            title=u'%s' % ugettext(all_months[month-1].strftime('%B')),
                            url='%s%04d/%02d/' % (page.get_absolute_url(), year, month),
                            tree_id=page.tree_id, # pretty funny tree hack
                            level=page.level+3,
                            language=getattr(page, 'language', settings.LANGUAGE_CODE),
                            slug='%04d/%02d' % (year, month),
                        )
                yield PagePretender(
                    title=u'%s' % year,
                    url='%s%s/' % (page.get_absolute_url(), year),
                    tree_id=page.tree_id, # pretty funny tree hack
                    level=page.level+2,
                    slug='%s' % year,
                    language=getattr(page, 'language', settings.LANGUAGE_CODE),
                    get_children=return_months,
                    )

        yield PagePretender(
            title=_('Archive'),
            url='#',
            tree_id=page.tree_id, # pretty funny tree hack
            level=page.level+1,
            slug='#',
            parent=page,
            language=getattr(page, 'language', settings.LANGUAGE_CODE),
            get_children=return_dates,
            )
