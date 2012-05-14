.. _widgets:

============
Blog Widgets
============

Widgets are a way tho show blog content outside of the main app. There are two ways of doing this:
Using content types or template tags.

Here we are going to describe some use-cases and how to implement them:

Teaser blog entries and FeinCMS pages on the landingpage
========================================================

.. image:: _static/widget_teaser.jpg

For a landing page that uses its own temlate anyway it makes sense to use a template tag.
Elephantblog comes with a template library called 'blog_widgets' that provides the function
get_frontpage which you could use like this::

    {% load i18n blog_widgets %}

    <div id="board-content" class="relative stepcarousel">
        {% get_frontpage %}
        <h1 id="helsinews">{% trans 'Neues von Helsi' %}</h1>
        <div class="belt">
            {% for item in entries %}
            <div class="board-page panel" title="{{ item.title }}" data-url="{{ item.get_absolute_url }}">
                {% feincms_render_region item "teaser" request %}
            </div>
            {% endfor %}
        </div>
    </div>

In this particular case we used the pageteaser content form the FeinCMS Contenttype Box Vol.1.
That one allows to combine FeinCMS pages and blog entries.
We also added a 'Teaser' region to both pages so the user can define manually what content
is displayed.


Adding categories or date breakdown to FeinCMS page navigation
==============================================================

.. image:: _static/widget_navigationextension.jpg

It is possible to add blog entries directly into the FeinCMS navigation path when using the blog
as ApplicationContent. You need to activate the navigation extensions for FeinCMS::

    Page.register_extensions('navigation', 'seo', 'titles', 'translations')

On the page where you add the 'Blog' ApplicationContent, also select a navigation extension

.. image:: _static/widget_naviextension_admin.jpg

In this example we used the CategoryAndDateNavigationExtension.
