from django.db.models.signals import pre_save
from django.apps import AppConfig


class ZionvotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zionvotes'

    def ready(self):
        from . import signals
