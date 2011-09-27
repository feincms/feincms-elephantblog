from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from elephantblog.models import Entry, entry_admin_update_fn


def pre_save_handler(sender, instance, **kwargs):
    if instance.is_active and not instance._old_is_active:
        instance.pinging = instance.QUEUED


def register(cls, admin_cls):
    cls.add_to_class('SLEEPING', 10)
    cls.add_to_class('QUEUED', 20)
    cls.add_to_class('SENT', 30)
    cls.add_to_class('UNKNOWN', 0)

    PINGING_CHOICES = (
        (cls.SLEEPING, _('sleeping')),
        (cls.QUEUED, _('queued')),
        (cls.SENT, _('sent')),
        (cls.UNKNOWN, _('unknown')),
    )

    cls.add_to_class('pinging', models.SmallIntegerField(_('ping'),
        editable=False, default=cls.SLEEPING, choices=PINGING_CHOICES)
    )

    admin_cls.actions.append(entry_admin_update_fn(_('queued'), {'pinging': cls.QUEUED},
        short_description=_('ping again')))

    signals.pre_save.connect(pre_save_handler, sender=cls)

