from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


class List(models.Model):
    id = models.BigIntegerField(primary_key=True)
    data = JSONField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    member_ids = ArrayField(models.BigIntegerField(), blank=True, null=True)
    subscriber_ids = ArrayField(models.BigIntegerField(), blank=True, null=True)

    member_names = ArrayField(models.CharField(max_length=20), blank=True, null=True)
    subscriber_names = ArrayField(models.CharField(max_length=20), blank=True, null=True)

    class Meta:
        ordering = ('-updated',)

    def member_count_ids(self):
        return self.member_ids and len(self.member_ids) or 0

    def member_count_names(self):
        return self.member_names and len(self.member_names) or 0

    def __unicode__(self):
        return self.data['name']
