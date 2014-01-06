from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _, ungettext


def _entry_admin_update_fn(new_state, new_state_dict, short_description=None):
    def _fn(self, request, queryset):
        rows_updated = queryset.update(**new_state_dict)

        self.message_user(request, ungettext(
            'One entry was successfully marked as %(state)s',
            '%(count)s entries were successfully marked as %(state)s',
            rows_updated) % {'state': new_state, 'count': rows_updated})

    if short_description:
        _fn.short_description = short_description
    return _fn


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

    cls.add_to_class(
        'pinging',
        models.SmallIntegerField(
            _('ping'),
            editable=False,
            default=cls.SLEEPING,
            choices=PINGING_CHOICES,
        )
    )

    if admin_cls:
        if not hasattr(admin_cls, 'actions'):
            setattr(admin_cls, 'actions', [])
        admin_cls.actions.append(_entry_admin_update_fn(
            _('queued'),
            {'pinging': cls.QUEUED},
            short_description=_('Ping Again')))

    pre_save.connect(pre_save_handler, sender=cls)
