"""
These are internal helpers. Do not rely on their presence.
"""

from __future__ import absolute_import, unicode_literals

from distutils.version import LooseVersion
from django import get_version
from django.template.loader import render_to_string


if LooseVersion(get_version()) < LooseVersion('1.10'):
    def ct_render_to_string(template, ctx, **kwargs):
        from django.template import RequestContext

        context_instance = kwargs.get('context')
        if context_instance is None and kwargs.get('request'):
            context_instance = RequestContext(kwargs['request'])

        return render_to_string(
            template,
            ctx,
            context_instance=context_instance)
else:
    def ct_render_to_string(template, ctx, **kwargs):
        return render_to_string(
            template,
            ctx,
            request=kwargs.get('request'))
