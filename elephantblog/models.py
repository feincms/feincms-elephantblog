"""
You need the following modules to use this blog:
Disqus: http://github.com/arthurk/django-disqus
Pinging: http://github.com/matthiask/pinging
Tagging: http://code.google.com/p/django-tagging/
"""

from datetime import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.core.urlresolvers import NoReverseMatch, reverse
from django.core.validators import ValidationError
from django.db import models
from django.db.models import signals, Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext, ungettext

from feincms import translations
from feincms.admin import item_editor
from feincms.content.application.models import app_reverse
from feincms.management.checker import check_database_schema
from feincms.models import Base
from feincms.utils.managers import ActiveAwareContentManagerMixin
from feincms.utils.queryset_transform import TransformQuerySet

from elephantblog import settings


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
        return self.active().filter(status=self.model.FRONT_PAGE)


EntryManager.add_to_active_filters(
    lambda queryset: queryset.filter(status__gte=Entry.CLEARED),
    key='cleared')
EntryManager.add_to_active_filters(
    Q(published_on__lte=datetime.now),
    key='published_on_past')


class Entry(Base):
    """
    Entries with a status of greater equal 50 are displayed
    if the current date is within the published date range.
    """

    DELETED = 10
    INACTIVE = 30
    NEEDS_REEDITING = 40
    CLEARED = 50
    FRONT_PAGE = 60

    STATUS_CHOICES = (
        (INACTIVE, _('inactive')),
        (CLEARED, _('cleared')),
        (FRONT_PAGE, _('front page')),
        (NEEDS_REEDITING, _('needs re-editing')),
        (DELETED, _('deleted')),
        )

    SLEEPING, QUEUED, SENT, UNKNOWN = 10, 20, 30, 0

    PINGING_CHOICES = (
        (SLEEPING, _('sleeping')),
        (QUEUED, _('queued')),
        (SENT, _('sent')),
        (UNKNOWN, _('unknown')),
        )

    title = models.CharField(_('title'), max_length=100, unique_for_date='published_on')
    slug = models.SlugField(_('slug'), max_length=100)
    status = models.SmallIntegerField(_('status'), choices=STATUS_CHOICES, default=CLEARED)
    published_on = models.DateTimeField(_('published on'), blank=True, null=True, default=datetime.now(),
        help_text=_('Will be updated automatically once the status is at least `cleared`.'))

    categories = models.ManyToManyField(Category, verbose_name=_('categories'),
        related_name='blogentries', null=True, blank=True)

    pinging = models.SmallIntegerField(_('ping'), editable=False, default=SLEEPING, choices=PINGING_CHOICES,
        help_text=_('Shows the status of the entry for the pinging management command.'))
    user = models.ForeignKey(User, editable=False, blank=True, related_name='blogentries', verbose_name=_('author'))
    last_changed = models.DateTimeField(_('last change'), auto_now=True, editable=False)

    class Meta:
        get_latest_by = 'published_on'
        ordering = ['-published_on']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    objects = EntryManager()

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self._old_status = self.status # stores if the entry has been published before it is being edited.

    def __unicode__(self):
        return unicode(self.title)

    def save(self, *args, **kwargs):
        if self.status >= self.CLEARED and self._old_status < self.CLEARED and self.published_on.date() <= datetime.now().date():
            self.published_on = datetime.now()
            self.pinging = self.QUEUED
        elif self.is_active and self.pinging < self.QUEUED:
            self.pinging = self.QUEUED
        try:
            self.full_clean() # kicks in if there are two entries that have the same title and are published on the same date.
        except ValidationError:
            self.title = self.title + ugettext(' again.')
        if not self.slug:
            self.slug = slugify(self.title)
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

    def active_status(self):
        try:
            if self.publication_end_date < datetime.now():
                return ugettext('expired')
        except:
            pass
        if self.published_on > datetime.now() and self.status >= self.CLEARED:
            return ugettext('on hold')
        else:
            return self.get_status_display()
    active_status.short_description = _('Status')

    def isactive(self):
        try:
            if self.publication_end_date < datetime.now():
                return False
        except Exception:
            pass
        if self.published_on > datetime.now() or self.status < self.CLEARED:
            return False
        else:
            return True
    isactive.short_description = _('active')
    isactive.boolean = True
    is_active = property(isactive)

    @property
    def featured(self):  #fits page extension featured
        return self.status >= FRONT_PAGE


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
    list_display = ['__unicode__', 'status', 'last_changed', 'isactive',
        'active_status', 'published_on', 'user', 'pinging']
    list_filter = ['status', 'published_on', 'categories', 'user']
    search_fields = ['title', 'slug']
    prepopulated_fields = {
        'slug': ('title',),
        }

    fieldsets = [
        [None, {
            'fields': [
                ('title', 'slug'),
                ('status', 'published_on'),
                'categories',
            ]
        }],
    ]

    raw_id_fields = []

    ping_again = entry_admin_update_fn(_('queued'), {'pinging': Entry.QUEUED},
        short_description=_('ping again'))

    mark_publish = entry_admin_update_fn(_('cleared'), {'status': Entry.CLEARED},
        short_description=_('mark publish'))

    mark_frontpage = entry_admin_update_fn(_('front-page'), {'status': Entry.FRONT_PAGE},
        short_description=_('mark frontpage'))

    mark_needs_reediting = entry_admin_update_fn(_('need re-editing'), {'status': Entry.NEEDS_REEDITING},
        short_description=_('mark re-edit'))

    mark_inactive = entry_admin_update_fn(_('inactive'), {'status': Entry.INACTIVE},
        short_description=_('mark inactive'))

    mark_delete = entry_admin_update_fn(_('deleted'), {'status': Entry.DELETED},
        short_description=_('remove'))

    actions = [
        mark_publish,
        mark_frontpage,
        mark_needs_reediting,
        mark_inactive,
        mark_delete,
        ping_again,
        ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


Entry.register_regions(*settings.BLOG_REGIONS)
