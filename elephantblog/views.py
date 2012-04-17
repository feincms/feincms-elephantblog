from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.cache import add_never_cache_headers
from django.views.generic import dates

from elephantblog.models import Category, Entry
from elephantblog.utils import entry_list_lookup_related

try:
    from towel import paginator
except ImportError:
    from django.core import paginator


__all__ = ('ArchiveIndexView', 'YearArchiveView', 'MonthArchiveView', 'DayArchiveView',
    'DateDetailView', 'CategoryArchiveIndexView')


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

    def get_queryset(self):
        return Entry.objects.active().transform(entry_list_lookup_related)

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(ElephantblogMixin, self).render_to_response(
            context, **response_kwargs)


class ArchiveIndexView(ElephantblogMixin, dates.ArchiveIndexView):
    paginator_class = paginator.Paginator
    paginate_by = 10
    date_field = 'published_on'
    template_name_suffix = '_archive'
    allow_empty = True


class YearArchiveView(ElephantblogMixin, dates.YearArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = 10
    date_field = 'published_on'
    make_object_list = True
    template_name_suffix = '_archive'


class MonthArchiveView(ElephantblogMixin, dates.MonthArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'
    template_name_suffix = '_archive'


class DayArchiveView(ElephantblogMixin, dates.DayArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'
    template_name_suffix = '_archive'


class DateDetailView(ElephantblogMixin, dates.DateDetailView):
    paginator_class = paginator.Paginator
    paginate_by = 10
    month_format = '%m'
    date_field = 'published_on'

    def get_queryset(self):
        if (self.request.user.is_authenticated() and self.request.user.is_staff
                and self.request.GET.get('eb_preview')):
            return Entry.objects.all()
        return Entry.objects.active()

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

        if not isinstance(response, HttpResponse):
            # For example in the case of inheritance 2.0
            return response

        for content in self.object.content.all_of_type(tuple(self.object._feincms_content_types_with_finalize)):
            r = content.finalize(self.request, response)
            if r:
                return r

        # Add never cache headers in case frontend editing is active
        if hasattr(self.request, "session") and self.request.session.get('frontend_editing', False):
            add_never_cache_headers(response)

        return response


class CategoryArchiveIndexView(ArchiveIndexView):
    template_name_suffix = '_archive'

    def get_queryset(self):
        self.category = get_object_or_404(Category, translations__slug=self.kwargs['slug'])

        queryset = super(CategoryArchiveIndexView, self).get_queryset()
        return queryset.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        return super(CategoryArchiveIndexView, self).get_context_data(
            category=self.category,
            **kwargs)
