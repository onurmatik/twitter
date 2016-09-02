from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from twitter.api import UserClient, StreamClient, TwitterAuthError


class User(DjangoUser):
    class Meta:
        proxy = True

    def get_client(self):
        return self.token.get_client()

    def get_stream_client(self):
        return self.token.get_stream_client()


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
        resource_family = resource_uri.split('/')[1]
        kwargs = {
            'rate_limit_status__%s__%s__remaining__gt' % (resource_family, resource_uri): 0,
        }
        token = Token.objects.filter(valid=True).filter(**kwargs).first()
        if token:
            resource = token.rate_limit_status[resource_family][resource_uri]
            resource['remaining'] -= 1
            token.save()
        else:
            self.reset_limits()
        return token

    def init_limits(self):
        for token in self.filter(valid=True).filter(rate_limit_status__isnull=True):
            token.fetch_rate_limit_status()

    def reset_limits(self):
        for token in self.filter(valid=True):
            token.reset_rate_limit_status()


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
