from django.contrib import admin
from twitter.users.models import TwitterUser
from twitter.lists.models import List


@admin.register(TwitterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    search_fields = ('data', 'id')
    list_display = (
        'name', 'time', 'protected', 'deactivated',
        'friend_count', 'fetched_friend_count', 'follower_count', 'fetched_follower_count',
    )
    list_filter = ('protected', 'deactivated',)
    actions = (
        'update_details', 'update_friends', 'update_followers',
        'create_friends_community', 'create_followers_community', 'create_connections_community',
        'create_friends_twitter_list', 'create_followers_twitter_list',
    )

    def update_details(self, request, queryset):
        for user in queryset:
            user.update_details()

    def update_friends(self, request, queryset):
        for user in queryset:
            user.update_friend_ids()

    def update_followers(self, request, queryset):
        for user in queryset:
            user.update_follower_ids()

    def create_friends_list(self):
        List.objects.create(

        )
