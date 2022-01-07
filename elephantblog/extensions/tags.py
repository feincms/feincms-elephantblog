from django.utils.translation import gettext_lazy as _
from feincms.extensions import Extension as FeincmsExtension
from taggit.managers import TaggableManager


class Extension(FeincmsExtension):
    def handle_model(self):
        self.model.add_to_class(
            "tags",
            TaggableManager(help_text=_("A comma-separated list of tags."), blank=True),
        )

    def handle_modeladmin(self, modeladmin):
        if hasattr(modeladmin, "add_extension_options"):
            modeladmin.add_extension_options("tags")
            modeladmin.extend_list("list_filter", ["tags"])
