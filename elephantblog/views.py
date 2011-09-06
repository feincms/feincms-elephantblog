from django.shortcuts import get_object_or_404
from django.views.generic import dates, list as list_

from elephantblog.models import Category, Entry
from elephantblog.utils import entry_list_lookup_related

try:
    from towel import paginator
except ImportError:
    from django.core import paginator


class ElephantblogMixin(object):
    """
    This mixin autodetects whether the blog is integrated through an
    ApplicationContent and automatically switches to inheritance2.0
    if that's the case.

    Additionally, it adds the view instance to the template context
    as ``view``.

    This requires at least FeinCMS v1.5.
    """

    def get_context_data(self, **kwargs):
        kwargs.update({'view': self})
        return super(ElephantblogMixin, self).get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(ElephantblogMixin, self).render_to_response(
            context, **response_kwargs)


class ListView(ElephantblogMixin, list_.ListView):
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    paginator_class = paginator.Paginator
    paginate_by = 10


class YearArchiveView(ElephantblogMixin, dates.YearArchiveView):
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    paginator_class = paginator.Paginator
    paginate_by = 10
    date_field = 'published_on'
    make_object_list = True


class MonthArchiveView(ElephantblogMixin, dates.MonthArchiveView):
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'


class DayArchiveView(ElephantblogMixin, dates.DayArchiveView):
    queryset = Entry.objects.active().transform(entry_list_lookup_related)
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'


class DateDetailView(ElephantblogMixin, dates.DateDetailView):
    queryset = Entry.objects.active()
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.prepare()
        if response:
            return response

        response = self.render_to_response(self.get_context_data(object=self.object))
        return self.finalize(response)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def prepare(self):
        """
        Prepare / pre-process content types. If this method returns anything,
        it is treated as a ``HttpResponse`` and handed back to the visitor.
        """

        http404 = None     # store eventual Http404 exceptions for re-raising,
                           # if no content type wants to handle the current self.request
        successful = False # did any content type successfully end processing?

        for content in self.object.content.all_of_type(tuple(self.object._feincms_content_types_with_process)):
            try:
                r = content.process(self.request, view=self)
                if r in (True, False):
                    successful = r
                elif r:
                    return r
            except Http404, e:
                http404 = e

        if not successful:
            if http404:
                # re-raise stored Http404 exception
                raise http404

            """ XXX This does not make sense in this context, does it?
            if not settings.FEINCMS_ALLOW_EXTRA_PATH and \
                    self.request._feincms_extra_context['extra_path'] != '/':
                raise Http404
            """

    def finalize(self, response):
        """
        Runs finalize() on content types having such a method, adds headers and
        returns the final response.
        """

        for content in self.object.content.all_of_type(tuple(self.object._feincms_content_types_with_finalize)):
            r = content.finalize(self.request, response)
            if r:
                return r

        # Add never cache headers in case frontend editing is active
        if hasattr(self.request, "session") and self.request.session.get('frontend_editing', False):
            add_never_cache_headers(response)

        return response


class CategoryListView(ElephantblogMixin, list_.ListView):
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
