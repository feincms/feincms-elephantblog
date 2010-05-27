from optparse import make_option
import sys
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

try:
    from elephantblog.models import Entry
    from pinging.models import PingedURL, PingServer
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
    option_list = NoArgsCommand.option_list + (
        make_option('--dry-run','-d',
            action='store_true',
            dest='dryrun',
            default=False,
            help='Does not send out any pings'),
        )
    help = 'Sends out a ping for new entries'
    
    def handle_noargs(self, **options):
        
        if PingServer.objects.count() == 0:
            raise CommandError('No servers defined.\nAdd at least one server in the admin interface.')
        
        batch = Entry.objects.active().filter(pinging__lte=Entry.QUEUED) #gets Entries for batch
        entry_id=[]
        for entry in batch:
            create_kwargs = {
                             'content_object': entry,
                             'weblogname': PINGING_WEBLOG_NAME,
                             'weblogurl': PINGING_WEBLOG_URL,
                             'changesurl': domain + ':/' + entry.get_absolute_url(),
                             }
            PingedURL.objects.create_for_servers(**create_kwargs)
            entry_id.append(entry.id)
                      
        if not options.get('dryrun'):    
            Entry.objects.filter(id__in=entry_id).update(pinging=Entry.SENT)    
            PingedURL.objects.process_pending()            
                
        PingedURL.objects.filter(created=datetime.now()-timedelta(days=7), 
                                     status=PingedURL.SUCCESSFUL).delete()
        bad = PingedURL.objects.filter(status__in=[PingedURL.ERROR, PingedURL.FAILED])
        if len(bad)>0:
            sys.stdout.write('Errors occured:')
            for entry in bad:
                Entry.objects.filter(id=entry.id).update(pinging=Entry.QUEUED)
                log = '%s %s in %s \n' %(entry.status, entry.message, entry.content_object)
                sys.stdout.write(log.encode('ascii', 'ignore'))
        else:
            sys.stdout.write('All pings successfull\n')
                
        