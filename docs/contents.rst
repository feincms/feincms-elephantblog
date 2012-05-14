.. _contents:

======================
Supplied Content Types
======================

While you can use all FeinCMS content types within elephantblog, the following content
types are specific to elephantblog and can be used within FeinCMS.

If you whish to show a list of top entries on the entry page of your website or promote
articles within your blog, have a look at the widgets_ section.


BlogEntryListContent
====================

This Content type shows a list view of all blog entries. It can be used
to show blog entries in FeinCMS pages.
If the 'featured only' flag is set, only posts which are marked as featured are shown.

The templates used by this content are 'content/entry_list.html' and
'content/entry_list_featured.html'. The latter one is optional. If it does not exist,
entry_list is used.

If you want to limit the entries shown to a certain number, just set that number for pagination
and remove the pagination part from the template.
