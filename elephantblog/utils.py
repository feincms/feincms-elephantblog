from elephantblog.models import Category, Entry


def entry_list_lookup_related(entry_qs):
    entry_dict = dict((e.pk, e) for e in entry_qs)

    if hasattr(Entry, 'richtextcontent_set'):
        for content in Entry.richtextcontent_set.related.model.objects.filter(
                parent__in=entry_dict.keys()).reverse():
            entry_dict[content.parent_id].first_richtext = content

    if hasattr(Entry, 'mediafilecontent_set'):
        for content in Entry.mediafilecontent_set.related.model.objects.filter(
                parent__in=entry_dict.keys(),
                mediafile__type='image').reverse().select_related('mediafile'):
            entry_dict[content.parent_id].first_image = content

    m2mfield = Entry._meta.get_field('categories')
    for category in Category.objects.filter(blogentries__in=entry_dict.keys()).extra(
            select={
                'entry_id': '%s.%s' % (m2mfield.m2m_db_table(), m2mfield.m2m_column_name()),
            }):
        entry = entry_dict[category.entry_id]
        if not hasattr(entry, 'fetched_categories'): entry.fetched_categories = []
        entry.fetched_categories.append(category)
