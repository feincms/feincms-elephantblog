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
from feincms.admin import editor
from feincms.content.application.models import app_reverse
from feincms.management.checker import check_database_schema
from feincms.models import Base
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

    def get_absolute_url(self):
        """
        Return the URL of a blog category

        Tries standalone first and falls back to ApplicationContent if
        the URL could not be reversed.
        """

        view_name = 'elephantblog_category_list'
        entry_dict = {
                      'category': self.translation.slug,
                      }
        try:
            return reverse(view_name, kwargs=entry_dict)
        except NoReverseMatch:
            return app_reverse(view_name, 'elephantblog.urls', kwargs=entry_dict)


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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(CategoryTranslation, self).save(*args, **kwargs)


class EntryManager(models.Manager):

    # A list of filters which are used to determine whether a page is active or not.
    # Extended for example in the datepublisher extension (date-based publishing and
    # un-publishing of pages)
    active_filters = {
        'cleared': lambda queryset: queryset.filter(published__gte=Entry.CLEARED),
        'publish_start': Q(published_on__lte=datetime.now),
        }

    def get_query_set(self):
        return TransformQuerySet(self.model, using=self._db)

    @classmethod
    def apply_active_filters(cls, queryset):
        for filt in cls.active_filters.values():
            if callable(filt):
                queryset = filt(queryset)
            else:
                queryset = queryset.filter(filt)

        return queryset

    def active(self):
        return self.apply_active_filters(self)

    def featured(self):
        return self.active().filter(published=self.model.FRONT_PAGE)


class Entry(Base):
    """
    Entries with a published status of greater equal 50 are displayed
    if the current date is within the published date range.
    """

    DELETED = 10
    INACTIVE = 30
    NEEDS_REEDITING = 40
    CLEARED = 50
    FRONT_PAGE = 60

    PUBLISHED_STATUS = (
        (INACTIVE,_('inactive')),
        (CLEARED,_('cleared')),
        (FRONT_PAGE,_('front page')),
        (NEEDS_REEDITING,_('needs re-editing')),
        (DELETED,_('deleted')),
        )

    SLEEPING, QUEUED, SENT, UNKNOWN = 10, 20, 30, 0

    PINGING_STATUS = (
        (SLEEPING, _('sleeping')),
        (QUEUED, _('queued')),
        (SENT, _('sent')),
        (UNKNOWN, _('unknown')),
        )

    PUBLISHED_STATUS_DICT = dict(PUBLISHED_STATUS)
    PINGING_STATUS_DICT = dict(PINGING_STATUS)

    user = models.ForeignKey(User, editable=False, blank=True, related_name="user_entry", verbose_name=_('author'))
    published = models.SmallIntegerField(_('publish'), choices=PUBLISHED_STATUS, default=CLEARED)
    pinging = models.SmallIntegerField(_('ping'), editable=False, default=SLEEPING, choices=PINGING_STATUS,
        help_text=_('Shows the status of the entry for the pinging management command.'))
    title = models.CharField(_('title'), max_length=100, unique_for_date='published_on')
    slug = models.SlugField(max_length=100)
    categories = models.ManyToManyField(Category, related_name="blogposts", null=True, blank=True)
    published_on = models.DateTimeField(_('published on'), blank=True, null=True, default=datetime.now(),
        help_text=_('Will be updated automatically once you tick the `published` checkbox above.'))

    last_changed = models.DateTimeField(_('last change'), auto_now=True, editable=False)

    class Meta:
        get_latest_by = 'published_on'
        ordering = ['-published_on']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    objects = EntryManager()

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self._old_published = self.published # stores if the entry has been published before it is being edited.

    def __unicode__(self):
        return unicode(self.title)

    def save(self, *args, **kwargs):
        if self.published >= self.CLEARED and self._old_published < self.CLEARED and self.published_on.date() <= datetime.now().date(): # only sets the publish date if the entry is published
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

    def get_absolute_url(self):
        """
        Return the URL of a blog entry

        Tries standalone first and falls back to ApplicationContent if
        the URL could not be reversed.
        """

        view_name = 'elephantblog.views.entry'
        entry_dict = {'year': "%04d" %self.published_on.year,
                      'month': "%02d" %self.published_on.month,
                      'day': "%02d" %self.published_on.day,
                      'slug': self.slug}
        try:
            return reverse(view_name, kwargs=entry_dict)
        except NoReverseMatch:
            return app_reverse(view_name, 'elephantblog.urls', kwargs=entry_dict)

    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, EntryAdmin)

    def active_status(self):
        try:
            if self.publication_end_date < datetime.now():
                return ugettext('expired')
        except:
            pass
        if self.published_on > datetime.now() and self.published >= self.CLEARED:
            return ugettext('on hold')
        else:
            return self.PUBLISHED_STATUS_DICT[self.published]

    active_status.short_description = _('Status')


    def isactive(self):
        try:
            if self.publication_end_date < datetime.now():
                return False
        except Exception:
            pass
        if self.published_on > datetime.now() or self.published < self.CLEARED:
            return False
        else:
            return True
    isactive.short_description = _('active')
    isactive.boolean = True
    is_active = property(isactive)

    @property
    def featured(self):  #fits page extension featured
        return self.published >= FRONT_PAGE


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


class EntryAdmin(editor.ItemEditor):
    date_hierarchy = 'published_on'
    list_display = ['__unicode__', 'published', 'last_changed', 'isactive',
        'active_status', 'published_on', 'user', 'pinging']
    list_filter = ['published', 'published_on', 'categories']
    search_fields = ['title', 'slug']
    prepopulated_fields = {
        'slug': ('title',),
        }

    fieldsets = [
        [None, {
            'fields': ['title', 'slug', 'categories', 'published_on']
        }],
    ]

    raw_id_fields = []

    ping_again = entry_admin_update_fn(_('queued'), {'pinging': Entry.QUEUED},
        short_description=_('ping again'))

    mark_publish = entry_admin_update_fn(_('cleared'), {'published': Entry.CLEARED},
        short_description=_('mark publish'))

    mark_frontpage = entry_admin_update_fn(_('front-page'), {'published': Entry.FRONT_PAGE},
        short_description=_('mark frontpage'))

    mark_needs_reediting = entry_admin_update_fn(_('need re-editing'), {'published': Entry.NEEDS_REEDITING},
        short_description=_('mark re-edit'))

    mark_inactive = entry_admin_update_fn(_('inactive'), {'published': Entry.INACTIVE},
        short_description=_('mark inactive'))

    mark_delete = entry_admin_update_fn(_('deleted'), {'published': Entry.DELETED},
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
