from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from twitter.tokens.models import Token


class List(models.Model):
    id = models.BigIntegerField(primary_key=True)
    data = JSONField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    member_ids = ArrayField(models.BigIntegerField(), blank=True, null=True)
    subscriber_ids = ArrayField(models.BigIntegerField(), blank=True, null=True)

    class Meta:
        ordering = ('-updated',)

    def member_count(self):
        return self.member_ids and len(self.member_ids) or '-'

    def subscriber_count(self):
        return self.subscriber_ids and len(self.subscriber_ids) or '-'

    def __unicode__(self):
        return self.data['name']

    def update_member_ids(self):
        token = Token.objects.get_for_resource('/lists/members')
        if token:
            client = token.get_client()
            response = client.api.lists.members.get(
                list_id=self.id,
                count=5000,
                include_entities=False,
            )
            self.member_ids = [user.id for user in response.data['users']]
            self.save()

    def update_subscriber_ids(self):
        token = Token.objects.get_for_resource('/lists/subscribers')
        if token:
            client = token.get_client()
            response = client.api.lists.subscribers.get(
                list_id=self.id,
                count=5000,
                include_entities=False,
            )
            self.member_ids = [user.id for user in response.data['users']]
            self.save()
