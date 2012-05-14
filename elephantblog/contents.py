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


class NewestEntriesContent(models.Model):
    """
    This content shows the newest blog entries. It is used mostly
    in index pages where summary of site content appear.
    """
    category = models.ForeignKey(Category, blank=True, null=True, related_name='+',
        verbose_name=_('category'), help_text=_('Only show entries from this category.'))
    count = models.IntegerField(verbose_name=_('item count'), default=5,
                                help_text=_('Entry count to show.'))

    class Meta:
        abstract = True # Required by FeinCMS, content types must be abstract
        verbose_name = _('newest entries content')
        verbose_name_plural = _('newest entries contents')

    def render(self, **kwargs):
        elist = Entry.objects.get_query_set().transform(entry_list_lookup_related)
        if self.category:
            elist = elist.filter(categories=self.category)
        elist = elist.order_by('-published_on')[:self.count]
        return render_to_string('content/elephantblog/newest_entries.html', {
            'content': self, # Not required but a convention followed by
                             # all of FeinCMS' bundled content types
            'entry_list': elist,
        })


class FeaturedEntriesContent(models.Model):
    """
    This content shows the featured blog entries.
    """
    count = models.IntegerField(verbose_name=_('item count'), default=5,
                                help_text=_('Entry count to show.'))

    class Meta:
        abstract = True # Required by FeinCMS, content types must be abstract
        verbose_name = _('featured entries content')
        verbose_name_plural = _('featured entries contents')

    def render(self, **kwargs):
        elist = Entry.objects.get_query_set().transform(entry_list_lookup_related)
        elist = elist.filter(is_featured__exact=True)[:self.count]
        return render_to_string('content/elephantblog/featured_entries.html', {
            'content': self, # Not required but a convention followed by
                             # all of FeinCMS' bundled content types
            'entry_list': elist,
        })


class QuoteContent(models.Model):
    """
    Quote content summarize part of an article in highlighted visual
    attractive way. It is widely used in other blog engines.
    """
    content = models.TextField(_('content'), max_length=255)
    position = models.IntegerField(_('position'), choices=(
      (0, _('block')),
      (1, _('left')),
      (2, _('right')),
    ))

    class Meta:
        abstract = True
        verbose_name = _('quote')
        verbose_name_plural = _('quotes')

    def render(self, **kwargs):
        return render_to_string([
            'content/quote/%s.html' % self.position,
            'content/quote/default.html',
            ], {'content': self})

    _pos_mapping = {1: 'left', 2: 'right'}
    def get_position_string(self):
        try:
            return self._pos_mapping[self.position]
        except:
            return ''
