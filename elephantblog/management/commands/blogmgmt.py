from optparse import make_option
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--cleanup', default=None, dest='clean',
            help='Removes deleted entries.')
    )