from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField


class ConnectionManager(models.Manager):
    def mutuals_of(self, user_id):
        return self.followers_of(user_id).intersection(
            self.friends_of(user_id)
        )


class Connection(models.Model):
    user_id = models.BigIntegerField(db_index=True)
    ids = ArrayField(models.BigIntegerField())
    next_cursor = models.CharField(max_length=20, db_index=True)
    previous_cursor = models.CharField(max_length=20, db_index=True)
    time = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class Friends(Connection):
    class Meta:
        verbose_name_plural = 'friends'


class Followers(Connection):
    class Meta:
        verbose_name_plural = 'followers'
