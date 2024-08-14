from random import shuffle

from django.db import models
from django.conf import settings

from zionvotes.helpers import random_slug
from zionvotes.fields import VoteSelectionField
from zionvotes.constants import METHOD_CHOICES, BALLOT_CHOICES, BALLOT_NEW


class Poll(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    open = models.BooleanField(default=False)
    closes_at = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def get_random_slug():
        return random_slug('p', 8)


class Race(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    poll_priority = models.IntegerField(null=True, blank=True, help_text="Force order when poll is shown")
    counting_method = models.CharField(choices=METHOD_CHOICES, max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    maximum_selections = models.IntegerField(null=True, blank=True)

    @staticmethod
    def get_random_slug():
        return random_slug('r', 12)

    @property
    def counting_method_name(self):
        return dict(METHOD_CHOICES).get(self.counting_method, "unset")

    @property
    def random_options(self):
        choices = list(self.choice_set.all())
        shuffle(choices)
        return choices


class Choice(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=255)

    @staticmethod
    def get_random_slug():
        return random_slug('ch', 12)

    def __str__(self):
        return self.name


class Ballot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    state = models.CharField(max_length=10, choices=BALLOT_CHOICES, default=BALLOT_NEW, blank=True)

    @staticmethod
    def get_random_slug():
        return random_slug('b', 20)


class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    ballot = models.ForeignKey('Ballot', on_delete=models.DO_NOTHING, null=True)
    race = models.ForeignKey('Race', on_delete=models.DO_NOTHING)
    selection = VoteSelectionField()
    vote_source = models.CharField(max_length=255, blank=True, null=True, help_text="Tracking identifier for externally loaded votes")

    @staticmethod
    def get_random_slug():
        return random_slug('v', 20)
