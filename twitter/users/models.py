from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from twitter.api import TwitterRateLimitError


class TwitterUser(models.Model):
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

    def get_client(self):
        # Get the Twitter REST client for the corresponding Django user, if exists
        user = User.objects.get(username=self.data['screen_name'])
        return user.get_client()

    def update_details(self, client=None):
        if not client:
            client = self.get_client()
        response = client.api.users.lookup.get(
            user_id=self.id,
            include_entities=False,
        )
        self.data = response.data[0]
        self.save()

    def _get_connections(self, api_call, max_rounds=15):  # 15 is the Twitter rate limit / 15 mins
        """
        fetches the user's friends / followers
        """

        ids = []
        next_cursor, i = -1, 0
        while next_cursor != 0 and i < max_rounds:
            try:
                response = api_call.ids.get(
                    user_id=self.id,
                    count=5000,
                    cursor=next_cursor,
                )
            except TwitterRateLimitError, e:
                sleep_time = retry_after_secs(e)
                print 'sleeping for %s secs' % sleep_time
                sleep(sleep_time)
            else:
                ids += response.data.ids
                next_cursor = response.data.next_cursor
            i += 1
        return ids

    def get_friends(self, client):
        if not self.friend_ids:
            ids = self._get_connections(client.api.friends)
            self.friend_ids = ids
            self.save()
        return self.friend_ids

    def get_followers(self, client):
        if not self.follower_ids:
            ids = self._get_connections(client.api.followers)
            self.follower_ids = ids
            self.save()
        return self.follower_ids

    def get_mutuals(self, client=None):
        if not client:
            client = self.get_client()
        mutuals = set(
            self.get_friends(client)
        ).intersection(
            self.get_followers(client)
        )
        return list(mutuals)

    def get_connection_ids(self):
        return set(self.friend_ids + self.follower_ids)

    def list_memberships(self):
        from twitter.lists.models import List
        return List.objects.filter(members__contains=self.data['id'])
