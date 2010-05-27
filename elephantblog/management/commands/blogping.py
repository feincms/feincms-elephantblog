#from optparse import make_option
#import os
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

try:
    from elephantblog.models import Entry
    from pinging.models import PingedURL
except ImportError, e:
    raise CommandError('%s. Could not import elephantblog or pinging apps.' %e)


PINGING_WEBLOG_NAME = settings.PINGING_WEBLOG_NAME
PINGING_WEBLOG_URL = settings.PINGING_WEBLOG_URL
try:
    domain = settings.FORCE_DOMAIN
except AttributeError:
    from django.contrib.sites.models import Site
    domain = Site.objects.get_current().domain




class Command(NoArgsCommand):

    help = 'Sends out a ping for new entries'
    
    def handle_noargs(self, **options):
        batch = Entry.objects.active().filter(pinging__lte=Entry.QUEUED) #gets Entries for batch
        for entry in batch:
            create_kwargs = {
                             'content_object': entry,
                             'weblogname': PINGING_WEBLOG_NAME,
                             'weblogurl': PINGING_WEBLOG_URL,
                             'changesurl': domain + ':/' + entry.get_absolute_url(),
                             }
            PingedURL.objects.create_for_servers(**create_kwargs)
            entry.pinging = Entry.SENT
            entry.save()
            
    PingedURL.objects.process_pending()
            
    PingedURL.objects.filter(created=datetime.now()-timedelta(days=7), 
                                 status=PingedURL.SUCCESSFUL).delete()
