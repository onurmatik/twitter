from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


class List(models.Model):
    id = models.BigIntegerField(primary_key=True)
    data = JSONField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    members = ArrayField(models.BigIntegerField(), blank=True, null=True)
    subscribers = ArrayField(models.BigIntegerField(), blank=True, null=True)

    class Meta:
        ordering = ('-updated',)

    def member_count(self):
        return self.members and len(self.members) or 0

    def __unicode__(self):
        return self.data['name']
