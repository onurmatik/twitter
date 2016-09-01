from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField


class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    data = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True)
