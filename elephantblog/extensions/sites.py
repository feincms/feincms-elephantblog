"""
Allows the blog to use the sites framework.
"""
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.db.models import ManyToManyField
from django.db.models import Q

def register(cls, admin_cls, *args):
    cls.add_to_class('sites', ManyToManyField(Site, blank=True, 
        help_text=_('The sites where the blogpost should appear.'), default=Site.objects.get_current()))

    cls.objects.active_filters.append(Q(sites=Site.objects.get_current()))

    def sites_admin(self):
        available_sites = self.sites.all()
        return u', '.join(u'%s' % site.name for site in available_sites)
    
    sites_admin.allow_tags = True
    sites_admin.short_description = _('Sites')
    cls.sites_admin = sites_admin

    admin_cls.show_on_top.append('sites')
    admin_cls.list_filter += ('sites',)
    admin_cls.list_display.append('sites_admin')
