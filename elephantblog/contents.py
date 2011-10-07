# coding=utf-8

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from elephantblog.models import Category, Entry
from elephantblog.utils import entry_list_lookup_related

try:
    # Load paginator with additional goodies form towel if possible
    from towel.paginator import Paginator, EmptyPage, PageNotAnInteger
except ImportError:
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BlogEntryListContent(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, related_name='+',
        verbose_name=_('category'), help_text=_('Only show entries from this category.'))
    paginate_by = models.PositiveIntegerField(_('paginate by'), default=0,
        help_text=_('Set to 0 to disable pagination.'))

    class Meta:
        abstract = True
        verbose_name = _('Blog entry list')
        verbose_name_plural = _('Blog entry lists')

    def process(self, request, **kwargs):
        entries = Entry.objects.active().transform(entry_list_lookup_related)

        if self.category:
            entries = entries.filter(categories=self.category)

        if self.paginate_by:
            paginator = Paginator(entries, self.paginate_by)
            page = request.GET.get('page', 1)
            try:
                self.entries = paginator.page(page).object_list
            except PageNotAnInteger:
                self.entries = paginator.page(1).object_list
            except EmptyPage:
                self.entries = paginator.page(paginator.num_pages).object_list

        else:
            self.entries = entries

    def render(self, **kwargs):
        return render_to_string('content/elephantblog/entry_list.html', {
            'content': self,
            })
