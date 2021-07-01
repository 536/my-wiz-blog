from django.apps import AppConfig


class WizConfig(AppConfig):
    name = 'wiz'

    def ready(self):
        from . import signals
