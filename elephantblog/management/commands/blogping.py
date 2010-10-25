from optparse import make_option
import sys
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from django.db.models import Q

try:
    from elephantblog.models import Entry, EntryManager
    from pinging.models import PingedURL, PingServer
except ImportError, e:
    raise CommandError('%s. Could not import elephantblog or pinging apps.' %e)

MAX_POSTS = 50
PINGING_WEBLOG_NAME = settings.PINGING_WEBLOG_NAME
PINGING_WEBLOG_URL = settings.PINGING_WEBLOG_URL
PINGING_WEBLOG_URI = settings.PINGING_WEBLOG_URI
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
            help='Does not send out any pings and does not change the database'),
        make_option('--nosend','-n',
            action='store_true',
            dest='nosend',
            default=False,
            help='Does not send out any pings'),
        )
    help = 'Sends out a ping for new entries'
    
    def handle_noargs(self, **options):
        
        if PingServer.objects.count() == 0:  # Test if a server is in the list.
            raise CommandError('No servers defined.\nAdd at least one server in the admin interface.')
        if 'sites' in Entry._feincms_extensions:
            self.use_sites = True
        
        if getattr(self, 'use_sites', False):
            active_filter = EntryManager.active_filters.copy()
            del active_filter['sites']
            active_filter.update({'pinging': Q(pinging__lte=Entry.QUEUED)})
            batch =  EntryManager.apply_active_filters(Entry.objects.all(), filter=active_filter)
        else:        
            batch = Entry.objects.active().filter(pinging__lte=Entry.QUEUED) #gets Entries for batch
        if len(batch) > MAX_POSTS:
            print 'More than ' + MAX_POSTS + 'posts. Aborting.'
            return False
        
        entry_id=[]
        
        for entry in batch:
            if getattr(self, 'use_sites', False):
                for site in entry.sites.all():
                    create_kwargs = {
                             'content_object': entry,
                             'weblogname': site.name,
                             'weblogurl': site.domain + ':/' + PINGING_WEBLOG_URL,
                             'changesurl': site.domain + ':/' + entry.get_absolute_url(),
                             }
                    if not options.get('dryrun'):  
                        PingedURL.objects.create_for_servers(**create_kwargs)
            else:                
                create_kwargs = {
                             'content_object': entry,
                             'weblogname': PINGING_WEBLOG_NAME,
                             'weblogurl': PINGING_WEBLOG_URL,
                             'changesurl': domain + ':/' + entry.get_absolute_url(),
                             }
                if not options.get('dryrun'):
                    PingedURL.objects.create_for_servers(**create_kwargs)
            entry_id.append(entry.id)
                      
        if not (options.get('dryrun') or options.get('nosend')):   
            Entry.objects.filter(id__in=entry_id).update(pinging=Entry.UNKNOWN)     
            PingedURL.objects.process_pending()            
            
                
        PingedURL.objects.filter(created=datetime.now()-timedelta(days=7), 
                                     status=PingedURL.SUCCESSFUL).delete()
        bad = PingedURL.objects.filter(status__in=[PingedURL.ERROR, PingedURL.FAILED])
        good = PingedURL.objects.filter(status=PingedURL.SUCCESSFUL)
        for entry in good:
            Entry.objects.filter(id=entry.content_object.id).update(pinging=Entry.SENT)
        if len(bad)>0:
            sys.stdout.write('Errors occured:')
            for entry in bad:
                Entry.objects.filter(id=entry.content_object.id).update(pinging=Entry.QUEUED)
                log = '%s %s in %s \n' %(entry.status, entry.message, entry.content_object)
                sys.stdout.write(log.encode('ascii', 'ignore'))
        else:
            sys.stdout.write('All pings successfull\n')
