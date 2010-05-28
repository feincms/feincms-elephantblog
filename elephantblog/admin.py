from django.contrib import admin

from elephantblog.models import Entry, EntryAdmin, Category, CategoryAdmin
import pinging.models as pinging

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
