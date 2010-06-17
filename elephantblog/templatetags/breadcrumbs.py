from django import template
from django.template import TemplateSyntaxError
import datetime
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _




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
        day.url = reverse('elephantblog_day', kwargs={'year':date.year, 'month':'%02d'%date.month, 'day':'%02d'%date.day}, current_app='elephantblog')
    if mode in ['month', 'day']:
        month = Link(date.strftime('%B')) #Locale full month name
        month.url =  reverse('elephantblog_month', kwargs={'year':date.year, 'month':'%02d'%date.month}, current_app='elephantblog')
    if mode in ['year', 'month', 'day']:
        year = Link(date.year)
        year.url = reverse('elephantblog_year', args=[date.year], current_app='elephantblog') 
    root = Link(_('All'))  #Needs ugettext    
    root.url = reverse('elephantblog_all', current_app='elephantblog')
    return {'root': root, 'year':year, 'month':month, 'day':day}

