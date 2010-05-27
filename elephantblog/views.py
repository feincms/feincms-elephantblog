# from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from feincms.views.generic import list_detail
from django.template import RequestContext
from django.shortcuts import render_to_response
# from tagging.models import Tag, TaggedItem
from elephantblog.models import Entry
from django.http import Http404
import datetime




def blog_detail(request, queryset, year, month, day, slug, **kwargs):
    entry = Entry.objects.select_related().get(published_on__year=year,
            published_on__month=month, published_on__day=day, slug=slug[:50])
    if not entry.isactive() and not request.user.is_authenticated():
        raise Http404
    else:     
        return render_to_response('entry_detail.html', {'entry':entry}, context_instance=RequestContext(request))

def archive_day(request, year, month, day, queryset, page=0, paginate_by=10, template_name='entry_archive_day.html', **kwargs):
    # Convert date to numeric format
    date = datetime.datetime.strptime('%s-%s-%s' %(year, month, day), '%Y-%m-%d')
    return list_detail.object_list(
      request,
      queryset = queryset.filter(published_on__year=date.year, published_on__month=date.month, published_on__day=date.day).order_by('-published_on',),
      paginate_by = paginate_by,
      page = page,
      template_name = template_name,
      **kwargs)

def archive_month(request, year, month, queryset, page=0, paginate_by=10, template_name='entry_archive_month.html', **kwargs):
    # Convert date to numeric format
    date = datetime.datetime.strptime('%s-%s' %(year, month), '%Y-%m')
    return list_detail.object_list(
      request,
      queryset = queryset.filter(published_on__year=date.year, published_on__month=date.month).order_by('-published_on',),
      paginate_by = paginate_by,
      page = page,
      template_name = template_name,
      **kwargs)
    
def archive_year(request, year, queryset, page=0, paginate_by=10, template_name='entry_archive_year.html', **kwargs):
    # Convert date to numeric format
    date = datetime.datetime.strptime('%s' %year, '%Y')
    return list_detail.object_list(
      request,
      queryset = queryset.filter(published_on__year=date.year).order_by('-published_on',),
      paginate_by = paginate_by,
      page = page,
      template_name = template_name,
      **kwargs)

def category_object_list(request, category, queryset, page=0, paginate_by=10, template_name='entry_list_category.html', **kwargs):
    print 'category list'
    return list_detail.object_list(
      request,
      queryset = queryset.filter(categories__translations__title=category).order_by('-published_on',),
      paginate_by = paginate_by,
      page = page,
      template_name = template_name,
      **kwargs)