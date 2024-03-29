from django.db import models
from django.utils.translation import get_language, gettext_lazy as _

from elephantblog.models import Category, Entry
from elephantblog.utils import entry_list_lookup_related


try:
    # Load paginator with additional goodies form towel if possible
    from towel.paginator import EmptyPage, PageNotAnInteger, Paginator
except ImportError:
    from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class BlogEntryListContent(models.Model):
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.CASCADE,
        verbose_name=_("category"),
        help_text=_("Only show entries from this category."),
    )
    paginate_by = models.PositiveIntegerField(
        _("entries per page"), default=0, help_text=_("Set to 0 to disable pagination.")
    )
    featured_only = models.BooleanField(
        _("featured only"),
        blank=True,
        default=False,
        help_text=_("Only show articles marked as featured"),
    )

    only_active_language = False

    class Meta:
        abstract = True
        verbose_name = _("Blog entry list")
        verbose_name_plural = _("Blog entry lists")

    def process(self, request, **kwargs):
        if self.featured_only:
            entries = Entry.objects.featured()
        else:
            entries = Entry.objects.active()

        if self.category:
            entries = entries.filter(categories=self.category)

        if self.only_active_language:
            entries = entries.filter(language=get_language())

        entries = entries.transform(entry_list_lookup_related)

        if self.paginate_by:
            paginator = Paginator(entries, self.paginate_by)
            page = request.GET.get("page", 1)
            try:
                self.entries = paginator.page(page)
            except PageNotAnInteger:
                self.entries = paginator.page(1)
            except EmptyPage:
                self.entries = paginator.page(paginator.num_pages)

        else:
            self.entries = entries

    def render(self, **kwargs):
        template_names = ["content/elephantblog/entry_list.html"]
        if self.featured_only:
            template_names.insert(0, "entry_list_featured.html")
        return template_names, {"content": self}


class BlogCategoryListContent(models.Model):
    show_empty_categories = models.BooleanField(_("show empty categories?"))

    class Meta:
        abstract = True
        verbose_name = _("Blog category list")
        verbose_name_plural = _("Blog category lists")

    def render(self, **kwargs):
        if self.show_empty_categories:
            categories = Category.objects.all()
        else:
            categories = Category.objects.exclude(blogentries__isnull=True)

        return (
            "content/elephantblog/category_list.html",
            {"content": self, "categories": categories},
        )
