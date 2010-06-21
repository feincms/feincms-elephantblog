from datetime import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals, Q
from django.utils.translation import ugettext_lazy as _, ugettext, get_language
from django.conf import settings
from feincms.admin import editor
from feincms.management.checker import check_database_schema
from feincms.models import Base
from django.core.validators import ValidationError
from feincms.translations import TranslatedObjectMixin, Translation, \
    TranslatedObjectManager
from django.template.defaultfilters import slugify


"""
Category is language-aware and connected to the Entry model via a many to many relationship.
It's easy to change the language of the models if the templates in admin/templates are copied to the application directory.

You need the following modules to use this blog:
Disqus: http://github.com/arthurk/django-disqus
Pinging: http://github.com/matthiask/pinging
Tagging: http://code.google.com/p/django-tagging/
"""

class Category(models.Model, TranslatedObjectMixin):

    ordering = models.SmallIntegerField(_('ordering'), default=0)

    def __unicode__(self):
        trans = None

        # This might be provided using a .extra() clause to avoid hundreds of extra queries:
        if hasattr(self, "preferred_translation"):
            trans = getattr(self, "preferred_translation", u"")
        else:
            try:
                trans = unicode(self.translation)
            except models.ObjectDoesNotExist:
                pass
            except AttributeError:
                pass

        if trans:
            return trans
        else:
            return _('Unnamed Category')

    def entries(self):
        return Entry.objects.filter(categories=self, language=get_language()).count()
    entries.short_description = _('Blog entries in category')

    objects = TranslatedObjectManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['-ordering',]


class CategoryTranslation(Translation(Category)):
    title = models.CharField(_('category title'), max_length=100)
    slug = models.SlugField(_('slug'),)
    description = models.CharField(_('description'), max_length=250, blank=True)

    class Meta:
        verbose_name = _('media file translation')
        verbose_name_plural = _('media file translations')
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
    CLEARED = 50
    active_filters = {'cleared' : Q(published__gte=CLEARED),
        'publish_start': Q(published_on__lte=datetime.now()),}



    @classmethod
    def apply_active_filters(cls, queryset, filter):
        cls.filters = filter.values()

        for filt in cls.filters:
            if callable(filt):
                queryset = filt(queryset)
            else:
                queryset = queryset.filter(filt)
        return queryset

    def active(self):
        return self.apply_active_filters(self, filter=self.active_filters)


    def featured(self):
        return self.published().filter(published=self.model.FRONT_PAGE)

"""
Entries with a published status of greater than 50 are displayed. If the current date is within the published date range.
"""

class Entry(Base):

    DELETED = 10
    INACTIVE = 30
    NEEDS_REEDITING = 40
    CLEARED = 50
    FRONT_PAGE = 60


    PUBLISHED_STATUS = (
    (INACTIVE,_('INACTIVE')),
    (CLEARED,_('CLEARED')),
    (FRONT_PAGE,_('FRONT PAGE')),
    (NEEDS_REEDITING,_('NEEDS RE-EDITING')),
    (DELETED,_('DELETED')),
    )

    SLEEPING, QUEUED, SENT, UNKNOWN = 10, 20, 30, 0

    PINGING_STATUS = (
    (SLEEPING, _('SLEEPING')),
    (QUEUED, _('QUEUED')),
    (SENT, _('SENT')),
    (UNKNOWN, _('UNKNOWN')),
    )

    published_status = {}
    for status in PUBLISHED_STATUS: # generate Tuple with status for display in admin interface.
        published_status.update({status[0]:status[1]})
    pinging_status = {}
    for status in PINGING_STATUS:
        pinging_status.update({status[0]:status[1]})

    user = models.ForeignKey(User, editable=False, blank=True, related_name="user_entry", verbose_name=_('author'))
    published = models.SmallIntegerField(_('publish'), choices=PUBLISHED_STATUS, default=CLEARED)
    pinging = models.SmallIntegerField(_('ping'), editable=False, default=SLEEPING, choices=PINGING_STATUS,
        help_text=_('Shows the status of the entry for the pinging management command.'))
    title = models.CharField(_('title'), max_length=100, unique_for_date='published_on', #needs a concrete date in the field published_on.
        help_text=_('This is used for the generated navigation, too.'))
    slug = models.SlugField(max_length=100, unique=True)
    categories = models.ManyToManyField(Category, related_name="blogpost", null=True, blank=True)
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
        return self.title

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

    @models.permalink
    def get_absolute_url(self):
        return ('elephantblog_entry_detail', (), {
                                          'year': "%04d" %self.published_on.year,
                                          'month': "%02d" %self.published_on.month,
                                          'day': "%02d" %self.published_on.day,
                                          'slug': self.slug})

    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, EntryAdmin, Category)

    def year(self):
        return "%04d" %self.published_on.year

    def month(self):
        return "%02d" %self.published_on.month

    def day(self):
        return "%02d" %self.published_on.day

    def active_status(self):
        try:
            if self.publication_end_date < datetime.now():
                return ugettext('EXPIRED')
        except:
            pass
        if self.published_on > datetime.now() and self.published >= self.CLEARED:
            return ugettext('ON HOLD')
        else:
            return self.published_status[self.published]
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

signals.post_syncdb.connect(check_database_schema(Entry, __name__), weak=False)

