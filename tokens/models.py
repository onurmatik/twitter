from __future__ import unicode_literals

import redis
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from api import UserClient, StreamClient, TwitterAuthError
from users.models import User


r = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
)

p = r.pubsub(
    ignore_subscribe_messages=True,
)


class Application(models.Model):
    name = models.CharField(max_length=150)
    consumer_key = models.CharField(max_length=100)
    consumer_secret = models.CharField(max_length=100)
    permission = models.CharField(
        max_length=1,
        choices=(
            ('r', 'read'),
            ('w', 'read & write'),
            ('m', 'read, write & messages'),
        ),
        default='r',
    )

    def __unicode__(self):
        return self.name


class TokenManager(models.Manager):
    def get_for_resource(self, resource_uri):
        resource_family = resource_uri.split('/')[0]
        kwargs = {
            'resources__%s__%s__remaining__gt' % (resource_family, resource_uri): 0,
        }
        token = Token.objects.filter(**kwargs).first()
        token.rate_limit_status[resource_family][resource_uri]['remaining'] -= 1
        token.save()
        if token.rate_limit_status[resource_family][resource_uri]['remaining'] == 0:
            token.update_rate_limit_status(resource_uri)
        return token


class Token(models.Model):
    app = models.ForeignKey(Application, blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)
    data = JSONField(blank=True, null=True)
    rate_limit_status = JSONField(blank=True, null=True)
    valid = models.BooleanField(default=True)

    objects = TokenManager()

    def __unicode__(self):
        return self.data['screen_name']

    def get_client(self):
        return UserClient(
            self.app.consumer_key or settings.CONSUMER_KEY,
            self.app.consumer_secret or settings.CONSUMER_SECRET,
            self.data['oauth_token'],
            self.data['oauth_token_secret'],
        )

    def get_stream_client(self):
        return StreamClient(
            self.app.consumer_key or settings.CONSUMER_KEY,
            self.app.consumer_secret or settings.CONSUMER_SECRET,
            self.data['oauth_token'],
            self.data['oauth_token_secret'],
        )

    def verify(self):
        try:
            self.get_client().api.account.verify_credentials.get(
                include_entities=False,
                skip_status=True,
                include_email=False,
            )
        except TwitterAuthError:
            self.valid = False
            self.save()

    def update_rate_limit_status(self, resources=None):
        try:
            response = self.get_client().api.application.rate_limit_status.get(
                resources=resources,
            )
        except Exception:
            pass
        else:
            self.rate_limit_status = response.resources
        self.save()
