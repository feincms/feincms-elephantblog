from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _, ungettext
from feincms.extensions import Extension as FeincmsExtension


class Extension(FeincmsExtension):
    """
    Adds the necessary field and properties for Pinging Status.
    """

    @staticmethod
    def pre_save_handler(sender, instance, **kwargs):
        if instance.is_active and not instance._old_is_active:
            instance.pinging = instance.QUEUED

    @staticmethod
    def _entry_admin_update_fn(new_state, new_state_dict,
                               short_description=None):
        def _fn(modeladmin, request, queryset):
            rows_updated = queryset.update(**new_state_dict)

            modeladmin.message_user(request, ungettext(
                'One entry was successfully marked as %(state)s',
                '%(count)s entries were successfully marked as %(state)s',
                rows_updated) % {'state': new_state, 'count': rows_updated})

        if short_description:
            _fn.short_description = short_description
        return _fn

    def handle_model(self):
        self.model.add_to_class('SLEEPING', 10)
        self.model.add_to_class('QUEUED', 20)
        self.model.add_to_class('SENT', 30)
        self.model.add_to_class('UNKNOWN', 0)

        PINGING_CHOICES = (
            (self.model.SLEEPING, _('sleeping')),
            (self.model.QUEUED, _('queued')),
            (self.model.SENT, _('sent')),
            (self.model.UNKNOWN, _('unknown')),
        )

        self.model.add_to_class(
            'pinging',
            models.SmallIntegerField(
                _('ping'),
                editable=False,
                default=self.model.SLEEPING,
                choices=PINGING_CHOICES,
            )
        )

        pre_save.connect(Extension.pre_save_handler, sender=self.model)

    def handle_modeladmin(self, modeladmin):
        actions = modeladmin.actions
        actions.append(Extension._entry_admin_update_fn(
            _('queued'),
            {'pinging': self.model.QUEUED},
            short_description=_('Ping Again')
        ))
