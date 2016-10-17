from django.contrib import admin
from twitter.connections.models import Friends, Followers


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    search_fields = ('user_id',)
    list_display = ('user_id', 'next_cursor', 'previous_cursor')


@admin.register(Followers)
class FollowerAdmin(admin.ModelAdmin):
    search_fields = ('user_id',)
    list_display = ('user_id', 'next_cursor', 'previous_cursor')
