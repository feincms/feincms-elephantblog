from django.contrib import admin

from elephantblog.models import Entry, Category
import pinging.models as pinging

class CategoryTranslationInline(admin.StackedInline):
    model   = CategoryTranslation
    max_num = len(settings.LANGUAGES)
    prepopulated_fields = {
        'slug': ('title',),
        }

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'entries']
    search_fields     = ['translations__title']
    inlines           = [CategoryTranslationInline]


class EntryAdmin(editor.ItemEditor):
    date_hierarchy = 'published_on'
    list_display = ['__unicode__', 'published', 'last_changed', 'isactive', 'active_status', 'published_on', 'user', 'pinging']
    list_filter = ('published','published_on')
    search_fields = ('title', 'slug',)
    prepopulated_fields = {
        'slug': ('title',),
        }

    show_on_top = ['title', 'published', 'categories']
    raw_id_fields = []

    def ping_again(self, request, queryset):
        rows_updated = queryset.update(pinging=Entry.QUEUED)
        if rows_updated == 1:
            message_bit = _("1 entry was")
        else:
            message_bit = _("%s entries were") % rows_updated
        self.message_user(request, _("%s successfully marked as queued.") % message_bit)
    ping_again.short_description = _('ping again')

    def mark_publish(self, request, queryset):
        rows_updated = queryset.update(published=Entry.CLEARED)
        if rows_updated == 1:
            message_bit = _("1 entry was")
        else:
            message_bit = _("%s entries were") % rows_updated
        self.message_user(request, _("%s successfully marked as cleared.") % message_bit)
    mark_publish.short_description = _('mark publish')

    def mark_frontpage(self, request, queryset):
        rows_updated = queryset.update(published=Entry.FRONT_PAGE)
        if rows_updated == 1:
            message_bit = _("1 entry was")
        else:
            message_bit = _("%s entries were") % rows_updated
        self.message_user(request, _("%s successfully marked as front-page.") % message_bit)
    mark_frontpage.short_description = _('mark frontpage')

    def mark_needs_reediting(self, request, queryset):
        rows_updated = queryset.update(published=Entry.NEEDS_REEDITING)
        if rows_updated == 1:
            message_bit = _("1 entry was")
        else:
            message_bit = _("%s entries were") % rows_updated
        self.message_user(request, _("%s successfully marked as need re-editing.") % message_bit)
    mark_needs_reediting.short_description = _('mark re-edit')

    def mark_inactive(self, request, queryset):
        rows_updated = queryset.update(published=Entry.INACTIVE)
        if rows_updated == 1:
            message_bit = _("1 entry was")
        else:
            message_bit = _("%s entries were") % rows_updated
        self.message_user(request, _("%s successfully marked as inactive.") % message_bit)
    mark_inactive.short_description = _('mark inactive')

    def mark_delete(self, request, queryset):
        rows_updated = queryset.update(published=Entry.DELETED)
        if rows_updated == 1:
            message_bit = _("1 entry was")
        else:
            message_bit = _("%s entries were") % rows_updated
        self.message_user(request, _("%s successfully marked as deleted.") % message_bit)
    mark_delete.short_description = _('remove')

    actions = (mark_publish, mark_frontpage, mark_needs_reediting, mark_inactive, mark_delete, ping_again)


    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


Entry.register_regions(
                ('main', _('Main content area')),
                )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
