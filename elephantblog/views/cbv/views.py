from django.shortcuts import get_object_or_404
from django.views.generic import dates, list as list_

from elephantblog.models import Category


class ApplicationContentInheritanceMixin(object):
    """
    This mixin autodetects whether the blog is integrated through an
    ApplicationContent and automatically switches to inheritance2.0
    if that's the case.

    This requires at least FeinCMS v1.5.
    """

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(ApplicationContentInheritanceMixin, self).render_to_response(
            context, **response_kwargs)


class ListView(ApplicationContentInheritanceMixin, list_.ListView):
    pass

class YearArchiveView(ApplicationContentInheritanceMixin, dates.YearArchiveView):
    pass

class MonthArchiveView(ApplicationContentInheritanceMixin, dates.MonthArchiveView):
    pass

class DayArchiveView(ApplicationContentInheritanceMixin, dates.DayArchiveView):
    pass

class DateDetailView(ApplicationContentInheritanceMixin, dates.DateDetailView):
    pass


class CategoryListView(ApplicationContentInheritanceMixin, list_.ListView):
    template_name_suffix = '_archive_category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, translations__slug=self.kwargs['slug'])

        queryset = super(CategoryListView, self).get_queryset()
        return queryset.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        return super(CategoryListView, self).get_context_data(
            category=self.category,
            **kwargs)
