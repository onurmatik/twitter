from django.contrib import admin
from twitter.lists.models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    search_fields = ('data', 'id')
    list_display = ('id', '__unicode__', 'updated', 'member_count', 'subscriber_count',)
    actions = ('update_members', 'update_subscribers',)

    def update_members(self, request, queryset):
        for l in queryset:
            l.update_member_ids()

    def update_subscribers(self, request, queryset):
        for l in queryset:
            l.update_subscriber_ids()
