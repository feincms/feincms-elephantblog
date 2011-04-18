from django import template
from django.template.loader import render_to_string

from feincms.templatetags.feincms_tags import _render_content, RenderRegionNode 
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

register = template.Library()

class BlogListRenderRegionNode(RenderRegionNode):

    def render(self, context):
        feincms_object = self.feincms_object.resolve(context)
        region = self.region.resolve(context)
        request = self.request.resolve(context)
        
        try:
            list_detail_content_object = feincms_object.content.all_of_type(RichTextContent)[0]
            list_detail_content = _render_content(list_detail_content_object, request=request, context=context)
        except IndexError:
            list_detail_content = u''
        
        '''
        first we try to find a mediafile in a MediaFileContent
        if we have no luck, we try to find a mediafiel in a GalleryContent
        '''
        try:
            media_file_content = feincms_object.content.all_of_type(MediaFileContent)[0].mediafile
        except IndexError:
            media_file_content = False
        
        context.update({
            'content': list_detail_content,
            'mediafile': media_file_content,
            'feincms_object': feincms_object,
        }) 
        
        return render_to_string('blog/entry_list_detail.html', context)

@register.tag
def blog_render_list_detail(parser, token):
    """
    {% blog_render_list_detail feincms_page "main" request %}
    """
    try:
        tag_name, feincms_object, region, request = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError, 'Invalid syntax for blog_render_list_detail: %s' % token.contents

    return BlogListRenderRegionNode(feincms_object, region, request)

@register.simple_tag
def add_media_to_feincms_object(request, media):
    #print request._feincms_appcontent_parameters
    return u''
