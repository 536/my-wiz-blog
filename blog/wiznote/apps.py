from django.apps import AppConfig


class WiznoteConfig(AppConfig):
    name = 'wiznote'

    def ready(self):
        from . import signals
