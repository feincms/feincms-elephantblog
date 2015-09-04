from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

from feincms import translations
from feincms.models import Base
from feincms.module.mixins import ContentModelMixin
from feincms.utils.managers import ActiveAwareContentManagerMixin
from feincms.utils.queryset_transform import TransformManager


@python_2_unicode_compatible
class Category(models.Model, translations.TranslatedObjectMixin):
    """
    Category is language-aware and connected to the Entry model via
    a many to many relationship.
    """

    ordering = models.SmallIntegerField(_('ordering'), default=0)

    objects = translations.TranslatedObjectManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['ordering']

    def __str__(self):
        try:
            translation = self.translation
        except models.ObjectDoesNotExist:
            return ugettext('Unnamed category')

        if translation:
            return '%s' % translation

        return ugettext('Unnamed category')


@python_2_unicode_compatible
class CategoryTranslation(translations.Translation(Category)):
    title = models.CharField(_('category title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.CharField(
        _('description'), max_length=250, blank=True)

    class Meta:
        verbose_name = _('category translation')
        verbose_name_plural = _('category translations')
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('elephantblog_category_detail', kwargs={
            'slug': self.slug,
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(CategoryTranslation, self).save(*args, **kwargs)


class EntryManager(ActiveAwareContentManagerMixin, TransformManager):
    def featured(self):
        return self.active().filter(is_featured=True)


EntryManager.add_to_active_filters(
    Q(is_active=True),
    key='cleared')

EntryManager.add_to_active_filters(
    lambda queryset: queryset.filter(published_on__lte=timezone.now()),
    key='published_on_past')


@python_2_unicode_compatible
class Entry(Base, ContentModelMixin):
    is_active = models.BooleanField(
        _('is active'), default=True, db_index=True)
    is_featured = models.BooleanField(
        _('is featured'), default=False, db_index=True)

    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(
        _('slug'), max_length=100,
        unique_for_date='published_on')
    author = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        related_name='blogentries',
        limit_choices_to={'is_staff': True}, verbose_name=_('author'))
    published_on = models.DateTimeField(
        _('published on'),
        blank=True, null=True, default=timezone.now, db_index=True,
        help_text=_(
            'Will be filled in automatically when entry gets published.'))
    last_changed = models.DateTimeField(
        _('last change'), auto_now=True, editable=False)

    categories = models.ManyToManyField(
        Category, verbose_name=_('categories'),
        related_name='blogentries', blank=True)

    objects = EntryManager()

    class Meta:
        get_latest_by = 'published_on'
        ordering = ['-published_on']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self._old_is_active = self.is_active

    def save(self, *args, **kwargs):
        if self.is_active and not self.published_on:
            self.published_on = timezone.now()

        super(Entry, self).save(*args, **kwargs)
    save.alters_data = True

    def get_absolute_url(self):
        # The view/template layer always works with visitors' local time.
        # Therefore, also generate localtime URLs, otherwise visitors will
        # hit 404s on blog entry URLs generated for them. Unfortunately, this
        # also means that you cannot send a permalink around half the globe
        # and expect it to work...
        # https://code.djangoproject.com/ticket/18794
        if settings.USE_TZ:
            pub_date = timezone.localtime(self.published_on)
        else:
            pub_date = self.published_on

        return reverse('elephantblog_entry_detail', kwargs={
            'year': pub_date.strftime('%Y'),
            'month': pub_date.strftime('%m'),
            'day': pub_date.strftime('%d'),
            'slug': self.slug,
        })

    @classmethod
    def register_extension(cls, register_fn):
        from .modeladmins import EntryAdmin
        register_fn(cls, EntryAdmin)
