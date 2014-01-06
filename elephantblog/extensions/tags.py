from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager


def register(cls, admin_cls):
    cls.add_to_class('tags', TaggableManager(
        help_text=_('A comma-separated list of tags.'), blank=True))

    if admin_cls:
        if hasattr(admin_cls, 'add_extension_options'):
            admin_cls.add_extension_options('tags')
