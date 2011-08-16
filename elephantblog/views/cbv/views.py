from django.shortcuts import get_object_or_404
from django.views.generic import dates, list as list_

from elephantblog.models import Category, Entry
from elephantblog.utils import entry_list_lookup_related

try:
    from towel import paginator
except ImportError:
    from django.core import paginator


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
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    paginator_class = paginator.Paginator
    paginate_by = 10


class YearArchiveView(ApplicationContentInheritanceMixin, dates.YearArchiveView):
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    paginator_class = paginator.Paginator
    paginate_by = 10
    date_field = 'published_on'
    make_object_list = True


class MonthArchiveView(ApplicationContentInheritanceMixin, dates.MonthArchiveView):
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'


class DayArchiveView(ApplicationContentInheritanceMixin, dates.DayArchiveView):
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'


class DateDetailView(ApplicationContentInheritanceMixin, dates.DateDetailView):
    queryset = Entry.objects.active()
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'


class CategoryListView(ApplicationContentInheritanceMixin, list_.ListView):
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    template_name_suffix = '_archive_category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, translations__slug=self.kwargs['slug'])

        queryset = super(CategoryListView, self).get_queryset()
        return queryset.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        return super(CategoryListView, self).get_context_data(
            category=self.category,
            **kwargs)
