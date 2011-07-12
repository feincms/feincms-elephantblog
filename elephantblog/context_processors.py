from django.utils import translation
from feincms.module.page.models import Page

def blog_page(request):
    """ Used to get the feincms page navigation within the blog app. """
    from feincms.module.page.models import Page
    try:
        return {'blog_page' : Page.objects.get(slug='blog', language=translation.get_language())}
    except:
        return {}