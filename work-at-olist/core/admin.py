from django.contrib import admin

from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'channel')


admin.site.register(models.Channel)
admin.site.register(models.Category, CategoryAdmin)
