from datetime import datetime, timedelta
from optparse import make_option
import sys

from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from elephantblog.models import Entry, EntryManager
from pinging.models import PingedURL, PingServer


MAX_POSTS = 50
PINGING_WEBLOG_NAME = settings.BLOG_TITLE
PINGING_WEBLOG_URL = settings.BLOG_DESCRIPTION

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
        if not PingServer.objects.count():
            raise CommandError('No servers defined.\nAdd at least one server in the admin interface.')

        self.use_sites = 'sites' in getattr(Entry, '_feincms_extensions', ())

        if self.use_sites and 'sites' in EntryManager.active_filters:
            # Process entries from all sites
            del EntryManager.active_filters['sites']

        EntryManager.active_filters['pinging'] = Q(pinging__lte=Entry.QUEUED)
        batch = Entry.objects.active()

        if len(batch) > MAX_POSTS:
            print 'More than ' + MAX_POSTS + 'posts. Aborting.'
            return False

        for entry in batch:
            if self.use_sites:
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

        if not (options.get('dryrun') or options.get('nosend')):
            batch.update(pinging=Entry.UNKNOWN)
            PingedURL.objects.process_pending()

        # Delete old entries (why?)
        PingedURL.objects.filter(
            created=datetime.now() - timedelta(days=7),
            status=PingedURL.SUCCESSFUL,
            ).delete()

        pingedurl_queryset = PingedURL.objects.filter(
            content_type=ContentType.objects.get_for_model(Entry))

        # Update entries which have been successfully pinged
        Entry.objects.filter(
            id__in=pingedurl_queryset.filter(status=PingedURL.SUCCESSFUL).values('object_id')
            ).update(pinging=Entry.SENT)

        # Update entries where pinging has failed (this time)
        Entry.objects.filter(
            id__in=pingedurl_queryset.filter(status__in=(PingedURL.ERROR, PingedURL.FAILED)).values('object_id')
            ).update(pinging=Entry.QUEUED)
