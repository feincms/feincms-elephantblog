from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals, Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext, ungettext

from feincms import translations
from feincms.admin import item_editor
from feincms.management.checker import check_database_schema
from feincms.models import Base
from feincms.utils.managers import ActiveAwareContentManagerMixin
from feincms.utils.queryset_transform import TransformQuerySet


class Category(models.Model, translations.TranslatedObjectMixin):
    """
    Category is language-aware and connected to the Entry model via
    a many to many relationship.
    """

    ordering = models.SmallIntegerField(_('ordering'), default=0)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['-ordering',]

    objects = translations.TranslatedObjectManager()

    def __unicode__(self):
        trans = translations.TranslatedObjectMixin.__unicode__(self)
        return trans or _('Unnamed category')


class CategoryTranslation(translations.Translation(Category)):
    title = models.CharField(_('category title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.CharField(_('description'), max_length=250, blank=True)

    class Meta:
        verbose_name = _('category translation')
        verbose_name_plural = _('category translations')
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('elephantblog_category_detail', (), {
            'slug': self.slug,
            })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(CategoryTranslation, self).save(*args, **kwargs)


class EntryManager(models.Manager, ActiveAwareContentManagerMixin):
    def get_query_set(self):
        return TransformQuerySet(self.model, using=self._db)

    def featured(self):
        return self.active().filter(is_featured=True)


EntryManager.add_to_active_filters(
    Q(is_active=True),
    key='cleared')
EntryManager.add_to_active_filters(
    lambda queryset: queryset.filter(published_on__lte=datetime.now),
    key='published_on_past')


class Entry(Base):
    is_active = models.BooleanField(_('is active'), default=True)
    is_featured = models.BooleanField(_('is featured'), default=False)

    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique_for_date='published_on')
    author = models.ForeignKey(User, related_name='blogentries', verbose_name=_('author'))

    published_on = models.DateTimeField(_('published on'), blank=True, null=True, default=datetime.now,
        help_text=_('Will be filled in automatically when entry gets published.'))
    last_changed = models.DateTimeField(_('last change'), auto_now=True, editable=False)

    categories = models.ManyToManyField(Category, verbose_name=_('categories'),
        related_name='blogentries', null=True, blank=True)

    class Meta:
        get_latest_by = 'published_on'
        ordering = ['-published_on']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    objects = EntryManager()

    def __unicode__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self._old_is_active = self.is_active

    def save(self, *args, **kwargs):
        if self.is_active and not self.published_on:
            self.published_on = datetime.now()

        super(Entry, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('elephantblog_entry_detail', (), {
            'year': self.published_on.strftime('%Y'),
            'month': self.published_on.strftime('%m'),
            'day': self.published_on.strftime('%d'),
            'slug': self.slug,
            })

    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, EntryAdmin)

signals.post_syncdb.connect(check_database_schema(Entry, __name__), weak=False)


def entry_admin_update_fn(new_state, new_state_dict, short_description=None):
    def _fn(self, request, queryset):
        rows_updated = queryset.update(**new_state)

        self.message_user(request, ungettext(
            'One entry was successfully marked as %(state)s',
            '%(count)s entries were successfully marked as %(state)s',
            rows_updated) % {'state': new_state, 'count': rows_updated})

    if short_description:
        _fn.short_description = short_description
    return _fn


class EntryAdmin(item_editor.ItemEditor):
    date_hierarchy = 'published_on'
    filter_horizontal = ['categories']
    list_display = ['title', 'is_active', 'is_featured',  'published_on', 'author']
    list_editable = ['is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'categories', 'author']
    raw_id_fields = ['author']
    search_fields = ['title', 'slug']
    prepopulated_fields = {
        'slug': ('title',),
        }

    fieldset_insertion_index = 1
    fieldsets = [
        [None, {
            'fields': [
                ('is_active', 'is_featured', 'published_on'),
                ('title', 'slug'),
                'author',
                'categories',
            ]
        }],
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    @classmethod
    def add_extension_options(cls, *f):
        if isinstance(f[-1], dict):     # called with a fieldset
            cls.fieldsets.insert(cls.fieldset_insertion_index, f)
            f[1]['classes'] = list(f[1].get('classes', []))
            f[1]['classes'].append('collapse')
        else:   # assume called with "other" fields
            cls.fieldsets[0][1]['fields'].extend(f)
