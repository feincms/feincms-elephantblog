from django import template

from elephantblog.models import Category, Entry
from django.db import connection


register = template.Library()


@register.assignment_tag
def elephantblog_categories():
    return Category.objects.all()


@register.assignment_tag
def elephantblog_archive_months():
    """
    Returns datetime objects of months that contains some entries.
    """
    return Entry.objects.active().dates('published_on', 'month', 'DESC')

@register.assignment_tag
def elephantblog_archive_years():
    """
    Returns datetime objects of years that contains some entries.
    """
    return Entry.objects.active().dates('published_on', 'year', 'DESC')

@register.assignment_tag
def elephantblog_tag_cloud():
    """
    Retrieves used categories and calculates sizes of font used
    based on usage count of particular category. Used for tag cloud.
    """
    from tagging.utils import calculate_cloud
    categories = _get_usage(Category, counts=True)
    return calculate_cloud(categories)

def _get_usage(model, counts=False):
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
    GROUP BY %(join_table)s.category_id
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

