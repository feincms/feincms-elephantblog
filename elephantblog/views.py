from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.http import Http404
from django.core import paginator
from django.contrib.auth import get_user_model
from django.db.models.fields import FieldDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from django.views.generic import dates

from feincms.module.mixins import ContentObjectMixin

from elephantblog.models import Category, Entry
from elephantblog.utils import entry_list_lookup_related


__all__ = (
    'ArchiveIndexView', 'YearArchiveView', 'MonthArchiveView',
    'DayArchiveView', 'DateDetailView', 'CategoryArchiveIndexView',
)


PAGINATE_BY = getattr(settings, 'BLOG_PAGINATE_BY', 10)


class ElephantblogMixin(object):
    """
    This mixin autodetects whether the blog is integrated through an
    ApplicationContent and automatically switches to inheritance2.0
    if that's the case.

    Additionally, it adds the view instance to the template context
    as ``view``.

    This requires at least FeinCMS v1.5.
    """

    entry_class = Entry

    def get_context_data(self, **kwargs):
        kwargs.update({'view': self})
        return super(ElephantblogMixin, self).get_context_data(**kwargs)

    def get_queryset(self):
        return self.entry_class.objects.active().transform(
            entry_list_lookup_related)

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(ElephantblogMixin, self).render_to_response(
            context, **response_kwargs)


class TranslationMixin(object):
    """
    #: Determines, whether list views should only display entries from
    #: the active language at a time. Requires the translations extension.
    """
    only_active_language = True

    def get_queryset(self):
        queryset = super(TranslationMixin, self).get_queryset()
        try:
            queryset.model._meta.get_field('language')
        except FieldDoesNotExist:
            return queryset
        else:
            if self.only_active_language:
                return queryset.filter(language=get_language())
            else:
                return queryset


class ArchiveIndexView(
        TranslationMixin, ElephantblogMixin, dates.ArchiveIndexView):
    paginator_class = paginator.Paginator
    paginate_by = PAGINATE_BY
    date_field = 'published_on'
    template_name_suffix = '_archive'
    allow_empty = True


class YearArchiveView(
        TranslationMixin, ElephantblogMixin, dates.YearArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = PAGINATE_BY
    date_field = 'published_on'
    make_object_list = True
    template_name_suffix = '_archive'


class MonthArchiveView(
        TranslationMixin, ElephantblogMixin, dates.MonthArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = PAGINATE_BY
    month_format = '%m'
    date_field = 'published_on'
    template_name_suffix = '_archive'


class DayArchiveView(
        TranslationMixin, ElephantblogMixin, dates.DayArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = PAGINATE_BY
    month_format = '%m'
    date_field = 'published_on'
    template_name_suffix = '_archive'


class DateDetailView(
        TranslationMixin, ContentObjectMixin, ElephantblogMixin,
        dates.DateDetailView):
    paginator_class = paginator.Paginator
    paginate_by = PAGINATE_BY
    month_format = '%m'
    date_field = 'published_on'
    context_object_name = 'entry'

    def get_queryset(self):
        if self.request.user.is_staff and self.request.GET.get('eb_preview'):
            return self.entry_class.objects.all()
        return super(DateDetailView, self).get_queryset()

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() not in self.http_method_names:
            return self.http_method_not_allowed(request, *args, **kwargs)
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.object = self.get_object()
        self.lookup_related()
        return self.handler(request, *args, **kwargs)

    def lookup_related(self):
        """
        This method mirrors ``entry_list_lookup_related``, and assigns
        ``first_richtext`` and ``first_image`` to the elephantblog entry
        if suitable contents can be found.
        """
        try:
            from feincms.contents import RichTextContent
            from feincms.module.medialibrary.contents import MediaFileContent
        except ImportError:  # FeinCMS<2
            from feincms.content.richtext.models import RichTextContent
            from feincms.content.medialibrary.models import MediaFileContent

        try:
            self.object.first_image = [
                mediafile
                for mediafile in self.object.content.all_of_type(
                    MediaFileContent)
                if mediafile.mediafile.type == 'image'][0]
        except IndexError:
            pass

        try:
            self.object.first_richtext = self.object.content.all_of_type(
                RichTextContent)[0]
        except IndexError:
            pass

    def get_next_or_none(self):
        try:
            return self.get_queryset().filter(
                published_on__gte=self.object.published_on,
            ).exclude(id=self.object.id).order_by('published_on')[0]
        except IndexError:
            return None

    def get_previous_or_none(self):
        try:
            return self.get_queryset().filter(
                published_on__lte=self.object.published_on,
            ).exclude(id=self.object.id).order_by('-published_on')[0]
        except IndexError:
            return None


class CategoryArchiveIndexView(ArchiveIndexView):
    template_name_suffix = '_archive'

    def get_queryset(self):
        slug = self.kwargs['slug']

        try:
            self.category = Category.objects.get(
                translations__slug=slug,
            )
        except Category.DoesNotExist:
            raise Http404('Category with slug %s does not exist' % slug)

        except Category.MultipleObjectsReturned:
            self.category = get_object_or_404(
                Category,
                translations__slug=slug,
                translations__language_code=get_language(),
            )

        queryset = super(CategoryArchiveIndexView, self).get_queryset()
        return queryset.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        return super(CategoryArchiveIndexView, self).get_context_data(
            category=self.category,
            **kwargs)


class AuthorArchiveIndexView(ArchiveIndexView):
    template_name_suffix = '_archive'

    def get_queryset(self):
        self.author = get_object_or_404(
            get_user_model(),
            is_staff=True,
            pk=self.kwargs['pk'],
        )
        return super(AuthorArchiveIndexView, self).get_queryset().filter(
            author=self.author,
        )

    def get_context_data(self, **kwargs):
        return super(AuthorArchiveIndexView, self).get_context_data(
            author=self.author,
            **kwargs)
