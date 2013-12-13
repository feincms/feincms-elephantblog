from django.contrib import admin

from elephantblog.modeladmins import CategoryAdmin, EntryAdmin
from elephantblog.models import Category, Entry


admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
