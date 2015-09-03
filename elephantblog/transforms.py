# coding: utf-8
from __future__ import absolute_import, unicode_literals
from elephantblog.models import Category, Entry

try:
    from feincms.contents import RichTextContent
    from feincms.module.medialibrary.contents import MediaFileContent
except ImportError:  # FeinCMS<2
    from feincms.content.richtext.models import RichTextContent
    from feincms.content.medialibrary.models import MediaFileContent


class BaseLookup(object):
    """ The base class for the transformation instructions
    """
    @staticmethod
    def lookup(entry_qs):
        """
        The main lookup function.
        Edit the models in place.
        Overwrite this.
        :param entry_qs: The Entry query set
        """
        pass


class RichTextMediaFileAndCategoriesLookup(BaseLookup):

    @staticmethod
    def lookup(entry_qs):
        entry_dict = dict((e.pk, e) for e in entry_qs)

        model = Entry.content_type_for(RichTextContent)
        if model:
            for content in model.objects.filter(
                    parent__in=entry_dict.keys(),
            ).reverse():
                entry_dict[content.parent_id].first_richtext = content

        model = Entry.content_type_for(MediaFileContent)
        if model:
            for content in model.objects.filter(
                    parent__in=entry_dict.keys(),
                    mediafile__type='image',
            ).reverse().select_related('mediafile'):
                entry_dict[content.parent_id].first_image = content

        m2mfield = Entry._meta.get_field('categories')
        categories = Category.objects.filter(
            blogentries__in=entry_dict.keys(),
        ).extra(
            select={
                'entry_id': '%s.%s' % (
                    m2mfield.m2m_db_table(), m2mfield.m2m_column_name()),
            },
        )

        for category in categories:
            entry = entry_dict[category.entry_id]
            if not hasattr(entry, 'fetched_categories'):
                entry.fetched_categories = []
            entry.fetched_categories.append(category)
