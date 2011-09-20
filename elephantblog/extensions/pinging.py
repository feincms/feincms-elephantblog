from django.db import models
from django.utils.translation import ugettext_lazy as _

from elephantblog.models import Entry, entry_admin_update_fn

SLEEPING, QUEUED, SENT, UNKNOWN = 10, 20, 30, 0

PINGING_CHOICES = (
    (SLEEPING, _('sleeping')),
    (QUEUED, _('queued')),
    (SENT, _('sent')),
    (UNKNOWN, _('unknown')),
    )


def register(cls, admin_cls):
    cls.add_to_class('pinging', models.SmallIntegerField(_('ping'),
        editable=False, default=SLEEPING, choices=PINGING_CHOICES)

    )

    admin_cls.actions.append(entry_admin_update_fn(_('queued'), {'pinging': QUEUED},
        short_description=_('ping again')))

