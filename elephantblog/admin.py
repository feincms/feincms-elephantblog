from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from elephantblog.models import Entry, EntryAdmin, Category, CategoryTranslation

from feincms.translations import admin_translationinline, short_language_code


CategoryTranslationInline = admin_translationinline(CategoryTranslation, prepopulated_fields={
    'slug': ('title',)})


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTranslationInline]
    list_display = ['__unicode__', 'entries']
    search_fields = ['translations__title']

    def entries(self, obj):
        if 'translations' in getattr(Entry, '_feincms_extensions', ()):
            return Entry.objects.filter(categories=obj, language=short_language_code()).count()
        return Entry.objects.filter(categories=obj)
    entries.short_description = _('Blog entries in category')


admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
