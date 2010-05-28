"""
Allows the blog to use the sites framework.
"""
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Q

sites = models.ManyToManyField(Site, blank=True)
def register(cls, admin_cls, *args):
    cls.add_to_class('sites', models.ManyToManyField(Site, _('Site'), blank=True, 
        help_text=_('The sites where the blogpost should appear.'), default=Site.objects.get_current()))

    cls.objects.active_filters.append(Q(sites=Site.objects.get_current()))

    admin_cls.show_on_top.append('sites')
    admin_cls.list_filter += ('sites',)
    admin_cls.list_display.append('sites')
