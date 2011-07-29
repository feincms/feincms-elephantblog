#coding=utf-8

from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from elephantblog.models import Category


class BlogGalleryTeaserWidget(models.Model):
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name = _('Blog Gallery Teaser Widget')
        verbose_name_plural = _('Blog Gallery Teaser Widgets')
        abstract = True

    def __unicode__(self):
        return self.category.__unicode__()

    @property
    def media(self):
        media = forms.Media()
        media.add_css({'all':('lib/fancybox/jquery.fancybox-1.3.1.css',
                              'content/gallery/classic.css')})
        media.add_js(('lib/fancybox/jquery.fancybox-1.3.1.pack.js',
                      'content/gallery/gallery.js'))
        return media

    def render(self, **kwargs):
        request = kwargs.get('request')
        entries = self.category.blogposts.select_related('gallerycontent', 'richtextcontent')
        for entry in entries:
            if entry.is_active:
                try:
                    entry.gallery = entry.gallerycontent_set.all()[0].gallery.ordered_images()[:3]
                except IndexError:
                    pass
                try:
                    entry.richtext = entry.richtextcontent_set.all()[0].render
                except IndexError:
                    pass
        return render_to_string('blog/widgets/galleryteaserwidget.html',
                                {'entries': entries },
                                context_instance=RequestContext(request))


class BlogEntryListContent(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, related_name='+',
        verbose_name=_('category'), help_text=_('Only show entries from this category.'))
    paginate_by = models.PositiveIntegerField(_('paginate by'), default=0,
        help_text=_('Set to 0 to disable pagination.'))

    class Meta:
        abstract = True

    @classmethod
    def initialize_type(cls, queryset):
        cls.queryset = queryset

    def process(self, request, **kwargs):
        entries = self.queryset._clone()

        if self.category:
            entries = entries.filter(categories=self.category)

        if self.paginate_by:
            paginator = Paginator(entries, paginate_by=self.paginate_by)
            page = request.GET.get('page')
            try:
                self.entries = paginator.page(page)
            except PageNotAnInteger:
                self.entries = paginator.page(1)
            except EmptyPage:
                self.entries = paginator.page(paginator.num_pages)

        else:
            self.entries = entries

    def render(self, **kwargs):
        return render_to_string('content/blog/entry_list.html', {
            'content': self,
            })
