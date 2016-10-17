from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models
from twitter.tokens.models import Token
from twitter.connections.models import Friends, Followers


class TwitterUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    data = JSONField(blank=True, null=True)

    protected = models.BooleanField(default=False)
    deactivated = models.BooleanField(default=False)

    time = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return self.data and self.data['screen_name'] or str(self.id)

    def __unicode__(self):
        return self.name

    def update_details(self, client=None):
        if not client:
            client = self.get_client()
        response = client.api.users.lookup.get(
            user_id=self.id,
            include_entities=False,
        )
        self.data = response.data[0]
        self.save()

    def update_friend_ids(self):
        cursor = -1
        while cursor != 0:
            token = Token.objects.get_for_resource('/friends/ids')
            if token:
                client = token.get_client()
                response = client.api.friends.ids.get(
                    user_id=self.id,
                    count=5000,
                    cursor=cursor,
                )
                Friends.objects.create(
                    user_id=self.id,
                    ids=response.data['ids'],
                    next_cursor=response.data['next_cursor'],
                    previous_cursor=response.data['previous_cursor'],
                )
                cursor = response.data['next_cursor']
            else:
                break

    def update_follower_ids(self):
        cursor = -1
        while cursor != 0:
            token = Token.objects.get_for_resource('/followers/ids')
            if token:
                client = token.get_client()
                response = client.api.friends.ids.get(
                    user_id=self.id,
                    count=5000,
                    cursor=cursor,
                )
                Followers.objects.create(
                    user_id=self.id,
                    ids=response.data['ids'],
                    next_cursor=response.data['next_cursor'],
                    previous_cursor=response.data['previous_cursor'],
                )
                cursor = response.data['next_cursor']
            else:
                break

    @property
    def friend_ids(self):
        # TODO: should only take the most recent ones into account
        qs = Friends.objects.filter(
            user_id=self.id,
        ).values_list('ids', flat=True)
        return set(sum(qs, []))

    @property
    def follower_ids(self):
        # TODO: should only take the most recent ones into account
        qs = Followers.objects.filter(
            user_id=self.id,
        ).values_list('ids', flat=True)
        return set(sum(qs, []))

    @property
    def friend_count(self):
        return self.data['friends_count']

    @property
    def follower_count(self):
        return self.data['followers_count']

    @property
    def fetched_friend_count(self):
        return len(self.friend_ids)

    @property
    def fetched_follower_count(self):
        return len(self.follower_ids)

    def list_memberships(self):
        # returns the lists the user is a member of
        from twitter.lists.models import List
        return List.objects.filter(members__contains=self.data['id'])
