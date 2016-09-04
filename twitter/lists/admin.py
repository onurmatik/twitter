from django.contrib import admin
from twitter.lists.models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    search_fields = ('data', 'id')
    list_display = ('id', '__unicode__', 'updated')
