from django.dispatch import receiver
from django.db.models.signals import pre_save

from zionvotes import models


def pre_save_slug(sender, instance, **kwargs):
    if instance.slug is None or instance.slug == '':
        instance.slug = instance.get_random_slug()


@receiver(pre_save, sender=models.Race)
def pre_save_poll(sender, instance, **kwargs):
    return pre_save_slug(sender, instance, **kwargs)


@receiver(pre_save, sender=models.Choice)
def pre_save_polloption(sender, instance, **kwargs):
    return pre_save_slug(sender, instance, **kwargs)
