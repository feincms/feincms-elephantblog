from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from feincms.extensions import Extension as FeincmsExtension


class Extension(FeincmsExtension):

    def handle_model(self):
        self.model.add_to_class('tags', TaggableManager(
            help_text=_('A comma-separated list of tags.'), blank=True))

    def handle_modeladmin(self, modeladmin):
        if hasattr(modeladmin, 'add_extension_options'):
            modeladmin.add_extension_options('tags')
