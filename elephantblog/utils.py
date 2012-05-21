from django.db import connection
import math

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

# ------------------------ code borrowed from django_tagging ------------------
LOGARITHMIC, LINEAR = 1, 2

def _calculate_thresholds(min_weight, max_weight, steps):
    delta = (max_weight - min_weight) / float(steps)
    return [min_weight + i * delta for i in range(1, steps + 1)]

def _calculate_tag_weight(weight, max_weight, distribution):
    """
    Logarithmic tag weight calculation is based on code from the
    `Tag Cloud`_ plugin for Mephisto, by Sven Fuchs.

    .. _`Tag Cloud`: http://www.artweb-design.de/projects/mephisto-plugin-tag-cloud
    """
    if distribution == LINEAR or max_weight == 1:
        return weight
    elif distribution == LOGARITHMIC:
        return math.log(weight) * max_weight / math.log(max_weight)
    raise ValueError(_('Invalid distribution algorithm specified: %s.') % distribution)

def calculate_cloud(tags, steps=4, distribution=LOGARITHMIC):
    """
    Add a ``font_size`` attribute to each tag according to the
    frequency of its use, as indicated by its ``count``
    attribute.

    ``steps`` defines the range of font sizes - ``font_size`` will
    be an integer between 1 and ``steps`` (inclusive).

    ``distribution`` defines the type of font size distribution
    algorithm which will be used - logarithmic or linear. It must be
    one of ``tagging.utils.LOGARITHMIC`` or ``tagging.utils.LINEAR``.
    """
    if len(tags) > 0:
        counts = [tag.count for tag in tags]
        min_weight = float(min(counts))
        max_weight = float(max(counts))
        thresholds = _calculate_thresholds(min_weight, max_weight, steps)
        for tag in tags:
            font_set = False
            tag_weight = _calculate_tag_weight(tag.count, max_weight, distribution)
            for i in range(steps):
                if not font_set and tag_weight <= thresholds[i]:
                    tag.font_size = i + 1
                    font_set = True
    return tags

def get_usage(model, counts=False):
    """
    Perform the custom SQL query for retrieve tags and their
    usage count.
    """
    model_table = model._meta.db_table
    join_table_name = Entry.categories.through._meta.db_table
    model_pk = '%s.%s' % (model_table, model._meta.pk.column)
    query = """
    SELECT DISTINCT %(model_pk)s%(count_sql)s
    FROM
        %(join_table)s
        INNER JOIN %(model_table)s
            ON %(join_table)s.category_id = %(model_pk)s
    GROUP BY %(model_pk)s
    """ % {
        'count_sql': counts and (', COUNT(%s) AS cnt' % model_pk) or '',
        'model_table': model_table,
        'model_pk': model_pk,
        'join_table': join_table_name,
    }

    cursor = connection.cursor()
    cursor.execute(query)
    categories = []
    for row in cursor.fetchall():
        t = model(*row[:1])
        if counts:
            t.count = row[1]
        categories.append(t)
    return categories

