from django.contrib import admin
from twitter.friendships.models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'type', 'time', 'count', 'next_cursor', 'previous_cursor',)
    search_fields = ('user_id', 'ids',)
    list_filter = ('type',)

