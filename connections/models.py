from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField


class ConnectionManager(models.Manager):
    def connections_of(self, user_id):
        # all connections, friends & followers
        qs = self.filter(
            user_id=user_id,
        ).values_list('ids', flat=True)
        return set(sum(qs, []))

    def friends_of(self, user_id):
        qs = self.filter(
            user_id=user_id,
            type=1,
        ).values_list('ids', flat=True)
        return set(sum(qs, []))

    def followers_of(self, user_id):
        qs = self.filter(
            user_id=user_id,
            type=2,
        ).values_list('ids', flat=True)
        return set(sum(qs, []))

    def mutuals_of(self, user_id):
        return self.followers_of(user_id).intersection(
            self.friends_of(user_id)
        )


class Connection(models.Model):
    user_id = models.BigIntegerField(db_index=True)
    type = models.PositiveSmallIntegerField(
        db_index=True,
        choices=(
            (1, 'friends'),
            (2, 'followers'),
        )
    )
    ids = models.ArrayField(models.BigIntegerField())
    next_cursor = models.BigIntegerField(db_index=True)
    previous_cursor = models.BigIntegerField(db_index=True)
    time = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = ConnectionManager()
