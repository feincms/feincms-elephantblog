from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from elephantblog import models

from feincms.translations import admin_translationinline


CategoryTranslationInline = admin_translationinline(
    models.CategoryTranslation,
    prepopulated_fields={
        'slug': ('title',)
        })


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTranslationInline]
    list_display = ['__unicode__', 'ordering', 'entries']
    list_editable = ['ordering']
    search_fields = ['translations__title']

    def entries(self, obj):
        return u', '.join(unicode(entry) for entry in
            models.Entry.objects.filter(categories=obj)) or '-'
    entries.short_description = _('Blog entries in category')


admin.site.register(models.Entry, models.EntryAdmin)
admin.site.register(models.Category, CategoryAdmin)
