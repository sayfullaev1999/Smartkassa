from django.apps import AppConfig


class SmartKassaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartkassa'

    def ready(self):
        from . import signals  # noqa:
