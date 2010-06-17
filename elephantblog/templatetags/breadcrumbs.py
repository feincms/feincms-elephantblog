import datetime

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.template import TemplateSyntaxError




register = template.Library()

class Link(object):
    def __init__(self, name):
        self.name = name
        self.url = ""
    

""" Creates a date-based drilldown as in the admin interface """
@register.inclusion_tag('blog/date_drilldown.html')
def drilldown(date, mode):
    if not isinstance(date, datetime.date):
        raise TemplateSyntaxError('date must be a datetime.date instance.')
    if not mode in ['all','year','month','day']:
        raise TemplateSyntaxError('mode must be one of [all, year, month, day].')
    all, year, month, day = None, None, None, None
    if mode == 'day':
        day = Link('%02d'%date.day)
        #day.url = reverse('elephantblog_list', kwargs={'year':date.year, 'month':'%02d'%date.month, 'day':'%02d'%date.day}, current_app='elephantblog')
        day.url = '%s%s/%02d/%02d/' % (reverse('elephantblog_list'), date.year, date.month, date.day)
    if mode in ['month', 'day']:
        month = Link(date.strftime('%B')) #Locale full month name
        #month.url =  reverse('elephantblog_list', kwargs={'year':date.year, 'month':'%02d'%date.month}, current_app='elephantblog')
        month.url = '%s%s/%02d/' % (reverse('elephantblog_list'), date.year, date.month)
    if mode in ['year', 'month', 'day']:
        year = Link(date.year)
        #year.url = reverse('elephantblog_list', kwargs={'year':date.year,}, current_app='elephantblog')
        year.url = '%s%s/' % (reverse('elephantblog_list'), date.year)
    root = Link(_('All'))  #Needs ugettext    
    root.url = reverse('elephantblog_list', current_app='elephantblog')
    return {'root': root, 'year':year, 'month':month, 'day':day}

