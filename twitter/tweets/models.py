from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField


class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    data = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True)

    def username(self):
        return self.data['user']['screen_name']

    def text(self):
        return self.data['text']

    def photo_urls(self):
        urls = []
        for entity in self.data['entities']:
            if 'media' in entity and entity['media']['type'] == 'photo':
                urls.append(entity['media']['expanded_url'])
        return urls

    def video_urls(self):
        urls = []
        for entity in self.data['extended_entities']:
            if entity['type'] == 'video':
                urls.append(entity['expanded_url'])
        return urls

    def has_photo(self):
        for entity in self.data['entities']:
            if 'media' in entity and entity['media']['type'] == 'photo':
                return True
        return False

    def has_video(self):
        for entity in self.data['extended_entities']:
            if entity['type'] == 'video':
                return True
        return False
