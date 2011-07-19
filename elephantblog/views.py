from datetime import date

from django.db.models.fields import FieldDoesNotExist
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from feincms.translations import short_language_code
# from tagging.models import Tag, TaggedItem
from django.core.exceptions import FieldError
from django.utils.datetime_safe import datetime

from django.conf import settings as djangosettings
from models import Entry
import settings

def entry(request, year, month, day, slug, language_code=None, template_name='blog/entry_detail.html', **kwargs):
    context={}

    entry = get_object_or_404(Entry.objects.select_related(),
                              published_on__year=year,
                               published_on__month=month,
                               published_on__day=day,
                               slug=slug)
    '''
    if this app runs without ApplicationContent integration we have to make sure
    the template extends from the basic_template so we prepend 'standalone/'
    to the template_name
    '''
    if recognize_app_content(request):
        template_name = '/'.join(['standalone', template_name,])

    if not entry.isactive() and not request.user.is_authenticated():
        raise Http404
    else:
        if getattr(entry, 'language', False):
            translation.activate(entry.language)
        extra_context = {
                         'entry':entry,
                         'date': date(int(year), int(month),int(day)),
                         'comments' : settings.BLOG_COMMENTS,
                         }

        return render_to_response(template_name, extra_context,
                                  context_instance=RequestContext(request))

""" Date views use object_list generic view due to pagination """

""" Define the options in the entry_dict of the url file. Copy the url file into your project. """

def entry_list(request, category=None, year=None, month=None, day=None, page=0,
               paginate_by=10, template_name='blog/entry_list.html', limit=None,
               exclude=None, **kwargs):
    extra_context = { 'request' : request }

    # blargh. rewrite this as soon as possible
    queryset = Entry.objects.active()
    try:
        field = Entry._meta.get_field('language')
        if len(getattr(djangosettings, 'LANGUAGES', ())) > 1:
            queryset = queryset.filter(language=short_language_code())
        else:
            try:
                queryset = queryset.filter(language=request._feincms_page.language)
            except AttributeError:
                pass
    except FieldDoesNotExist:
        pass

    """ You can define a dict of fields and values to exclude. """
    if exclude:
        queryset = queryset.exclude(**exclude)
    if limit:
        queryset = queryset[:limit]
    if category:
        queryset = queryset.filter(categories__translations__slug=category)
        extra_context.update({'category': category})
    if year:
        queryset = queryset.filter(published_on__year=int(year))
        extra_context.update({'drilldown_mode': 'year', 'title' : year })
    else:
        year = datetime.now().year
    if month:
        # display month as full word.
        from django.template import defaultfilters
        queryset = queryset.filter(published_on__month=int(month))
        extra_context.update({'drilldown_mode': 'month', 'title' : defaultfilters.date(date(int(year), int(month), 1), 'E Y')})
    else:
        month = datetime.now().month
    if day:
        from django.contrib.humanize.templatetags.humanize import naturalday
        queryset = queryset.filter(published_on__day=int(day))
        extra_context.update({'drilldown_mode': 'day', 'title' : naturalday(date(int(year), int(month), int(day))) })
    else:
        day = 1

    extra_context.update({'date':date(int(year), int(month), int(day)),
                          'comments' : settings.BLOG_COMMENTS})

    '''
    if this app runs without ApplicationContent integration we have to make sure
    the template extends from the basic_template so we prepend 'standalone/'
    to the template_name
    '''
    if recognize_app_content(request):
        template_name = '/'.join(['standalone', template_name,])
        #print request._feincms_extra_context
        from django.views.generic import list_detail
    else:
        from feincms.views.generic import list_detail

    return list_detail.object_list(
      request,
      queryset = queryset,
      paginate_by = paginate_by,
      page = page,
      template_name = template_name,
      extra_context = extra_context,
      **kwargs)

def recognize_app_content(request):
    return getattr(request, '_feincms_appcontent_parameters', False) == False and not getattr(request, '_feincms_extra_context',{}).has_key('in_appcontent_subpage')
