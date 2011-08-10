from django.views.generic import dates, list as list_


class ApplicationContentInheritanceMixin(object):
    """
    This mixin autodetects whether the blog is integrated through an
    ApplicationContent and automatically switches to inheritance2.0
    if that's the case.

    This requires at least FeinCMS v1.5.
    """

    def render_to_response(self, context, **response_kwargs):
        use_inheritance_20 = False

        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            use_inheritance_20 = True

        if use_inheritance_20:
            return self.get_template_names(), context

        return super(ApplicationContentInheritanceMixin, self).render_to_response(
            context, **response_kwargs)


class ListView(ApplicationContentInheritanceMixin, list_.ListView):
    pass

class YearArchiveView(ApplicationContentInheritanceMixin, dates.YearArchiveView):
    pass

class MonthArchiveView(ApplicationContentInheritanceMixin, dates.MonthArchiveView):
    pass

class DayArchiveView(ApplicationContentInheritanceMixin, dates.DayArchiveView):
    pass

class DateDetailView(ApplicationContentInheritanceMixin, dates.DateDetailView):
    pass
