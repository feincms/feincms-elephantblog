from django.utils.translation import ugettext_lazy as _

try:
    from taggit.managers import TaggableManager
except ImportError:
    raise Exception('django-taggit must be installed to use this extension')
    
def register(cls, admin_cls):
    cls.add_to_class('tags', TaggableManager(
        help_text=_('A comma-separated list of tags.')))
    admin_cls.fieldsets[0][1].get('fields').append('tags')
