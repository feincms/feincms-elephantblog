from feincms.module.page.models import Page
from feincms.translations import short_language_code


def blog_page(request):
    """ Used to get the feincms page navigation within the blog app. """
    from feincms.module.page.models import Page
        return {'blog_page': Page.objects.get(slug='blog', language=short_language_code())}
    except:
        try:
            return {'blog_page': Page.objects.get(slug='blog')}
        except:
            return {}
