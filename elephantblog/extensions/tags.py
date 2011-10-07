from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager


def register(cls, admin_cls):
    cls.add_to_class('tags', TaggableManager(
        help_text=_('A comma-separated list of tags.'), blank=True))
    admin_cls.fieldsets[0][1].get('fields').append('tags')
