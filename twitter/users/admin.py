from django.contrib import admin
from twitter.users.models import TwitterUser
from twitter.lists.models import List


@admin.register(TwitterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    search_fields = ('data', 'id')
    list_display = ('name', 'time', 'protected', 'deactivated', 'friend_count', 'follower_count',)
    list_filter = ('protected', 'deactivated',)
    actions = ('create_members_community',)

    def create_followers_list(self, request, queryset):
        member_ids = []
        list_names = []
        for l in queryset:
            member_ids += l.member_ids
            list_names.append(l.data['name'])
        List.objects.create(
            name='Followers of %s' % ', '.join(list_names),
            member_ids=member_ids,
            owner=request.user,
        )
