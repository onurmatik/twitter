from django.contrib import admin
from twitter.users.models import TwitterUser


@admin.register(TwitterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    search_fields = ('data', 'id')
    list_display = ('name', 'time', 'protected', 'deactivated',)
    list_filter = ('protected', 'deactivated',)
