from datetime import date

from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from feincms.translations import short_language_code
# from tagging.models import Tag, TaggedItem
from django.core.exceptions import FieldError

from feincms.views.generic import list_detail

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
        template_name = '/'.join('standalone', template_name)
    
    if not entry.isactive() and not request.user.is_authenticated():
        raise Http404
    else:
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
               language_code=None, exclude=None, **kwargs):
    extra_context = {}

    if language_code:
        queryset = Entry.objects.active().filter(language=language_code)
    else:
        try:
            language_code = request._feincms_page.language
            queryset = Entry.objects.active().filter(language=language_code)
        except (AttributeError, FieldError):
            queryset = Entry.objects.active()
        """ You can define a dict of fields and values to exclude. """
    if exclude:
        queryset = queryset.exclude(**exclude)
    if limit:
        queryset = queryset[:limit]
    if category:
        queryset = queryset.filter(categories__translations__title=category)
        extra_context.update({'category': category})
    if year:
        queryset = queryset.filter(published_on__year=int(year))
        extra_context.update({'drilldown_mode': 'year', 'title' : _('entries of the year')})
    else:
        year=1
    if month:
        queryset = queryset.filter(published_on__month=int(month))
        extra_context.update({'drilldown_mode': 'month', 'title' : _('entries of the month')})
    else:
        month=1
    if day:
        queryset = queryset.filter(published_on__day=int(day))
        extra_context.update({'drilldown_mode': 'day', 'title' : _('entries of the year')})
    else:
        day=1
    
    extra_context.update({'date':date(int(year), int(month), int(day)),
                          'comments' : settings.BLOG_COMMENTS})
    
    '''
    if this app runs without ApplicationContent integration we have to make sure
    the template extends from the basic_template so we prepend 'standalone/'
    to the template_name
    '''
    if recognize_app_content(request):
        template_name = '/'.join(['standalone', template_name,])
        print request._feincms_extra_context
    
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