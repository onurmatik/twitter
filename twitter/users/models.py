from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models


class TwitterUserManager(models.Manager):
    def incomplete_friend_list(self):
        #return self.filter(data__friends_count__gt=)
        pass


class TwitterUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    data = JSONField(blank=True, null=True)

    protected = models.BooleanField(default=False)
    deactivated = models.BooleanField(default=False)

    friend_ids = ArrayField(models.BigIntegerField(), blank=True, null=True)
    follower_ids = ArrayField(models.BigIntegerField(), blank=True, null=True)

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

    def update_connection_ids(self):
        # get the connections from the Friendship app
        #friends =
        self.friend_ids = list(set())

    def get_connection_ids(self):
        return set(self.friend_ids + self.follower_ids)

    def is_friend_list_complete(self):
        return self.data['friends_count'] == len(self.friend_ids)

    def is_follower_list_complete(self):
        return self.data['followers_count'] == len(self.follower_ids)

    def list_memberships(self):
        # returns the lists the user is a member of
        from twitter.lists.models import List
        return List.objects.filter(members__contains=self.data['id'])

    @property
    def friend_count(self):
        return self.friend_ids and len(self.friend_ids) or '-'

    @property
    def follower_count(self):
        return self.follower_ids and len(self.follower_ids) or '-'
